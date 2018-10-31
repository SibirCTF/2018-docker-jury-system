CREATE TABLE IF NOT EXISTS `flags` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `serviceid` int UNSIGNED DEFAULT NULL,
  `flag_id` varchar(50) DEFAULT NULL,
  `flag` varchar(36) DEFAULT NULL,
  `teamid` varchar(300) DEFAULT NULL,
  `date_start` bigint DEFAULT NULL,
  `date_end` bigint DEFAULT NULL,
  `team_stole` int UNSIGNED DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX( `teamid`, `team_stole`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `flags_live` (
  `id` int NOT NULL AUTO_INCREMENT,
  `serviceid` int UNSIGNED DEFAULT NULL,
  `flag_id` varchar(50) DEFAULT NULL,
  `flag` varchar(36) DEFAULT NULL,
  `teamid` int UNSIGNED DEFAULT NULL,
  `date_start` bigint DEFAULT NULL,
  `date_end` bigint DEFAULT NULL,
  `team_stole` int UNSIGNED DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
