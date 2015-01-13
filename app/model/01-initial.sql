CREATE TABLE `pb_user` (
  `_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'User ID',
  `_unique_id` varchar(20) NOT NULL COMMENT 'Unique ID supplied by client to identify a user',
  `_ts_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'User signup time',
  PRIMARY KEY (`_id`),
  UNIQUE KEY `UNIQ_unique_id` (`_unique_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `pb_user_session` (
  `_user_id` int(10) unsigned NOT NULL COMMENT 'User ID',
  `_session_hash` varchar(100) NOT NULL COMMENT 'MD5 hash of the user session',
  `_ts_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Time at which session was created',
  KEY `FK_user_session` (`_user_id`),
  CONSTRAINT `FK_user_session` FOREIGN KEY (`_user_id`) REFERENCES `pb_user` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `pb_tournament` (
  `_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'Tournament ID',
  `_ts_start` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Time at which tournament was initialized',
  `_ts_end` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'Time at which tournament ends',
  `_is_active` int(2) NOT NULL DEFAULT '1' COMMENT 'Is the tournament active',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `pb_game` (
  `_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'Game ID',
  `_tournament_id` int(10) DEFAULT NULL COMMENT 'Tournament to which this game belongs',
  `_data` varchar(1000) DEFAULT NULL COMMENT 'Game data to be sent to clients',
  `_rows` int(10) unsigned NOT NULL COMMENT 'Number of rows in this game',
  `_columns` int(10) NOT NULL COMMENT 'Number of columns in this game',
  PRIMARY KEY (`_id`),
  KEY `FK_game_tournament` (`_tournament_id`),
  CONSTRAINT `FK_game_tournament` FOREIGN KEY (`_tournament_id`) REFERENCES `pb_tournament` (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `pb_game_move` (
  `_game_id` int(10) NOT NULL COMMENT 'Game ID',
  `_user_id` int(10) unsigned NOT NULL COMMENT 'User id',
  `_game_moves` varchar(1000) NOT NULL COMMENT 'Game result',
  `_score` int(10) NOT NULL COMMENT 'Score for the current game',
  `_ts_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Time at which the result was last set',
  UNIQUE KEY `UNIQ_user_game` (`_game_id`,`_user_id`),
  KEY `FK_game_user` (`_user_id`),
  CONSTRAINT `FK_game_move` FOREIGN KEY (`_game_id`) REFERENCES `pb_game` (`_id`),
  CONSTRAINT `FK_game_user` FOREIGN KEY (`_user_id`) REFERENCES `pb_user` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `pb_device_notification` (
  `_session_hash` varchar(100) NOT NULL COMMENT 'Session for which notification token is saved',
  `_notification_token` varchar(100) NOT NULL COMMENT 'Notification token for the corresponding server',
  `_ts_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Time at which token was last updated',
  PRIMARY KEY (`_session_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `pb_subscribe_invite` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Auto ID',
  `_email` varchar(100) NOT NULL COMMENT 'Users email',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;