CREATE SCHEMA IF NOT EXISTS `twitter` DEFAULT CHARACTER SET utf8mb4;
USE `twitter` ;

CREATE TABLE IF NOT EXISTS `tweet` (
  `id` BIGINT NOT NULL,
  `text` VARCHAR(560) NULL,
  `created_at` DATE NULL,
  `author_id` BIGINT NULL,
  `like_count` INT NULL,
  `retweet_count` INT NULL,
  `reply_count` INT NULL,
  `quote_count` INT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `account` (
  `id` BIGINT NOT NULL,
  `username` VARCHAR(15) NULL,
  `description` VARCHAR(160) NULL,
  `followers_count` INT NULL,
  `following_count` INT NULL,
  `tweet_count` INT NULL,
  `listed_count` INT NULL,
  `verified` TINYINT NULL,
  `created_at` DATE NULL,
  PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `retweet` (
  `id_retweeter` BIGINT NOT NULL,
  `id_retweeted` BIGINT NOT NULL,
  PRIMARY KEY (`id_retweeter`, `id_retweeted`),
  FOREIGN KEY (`id_retweeter`) REFERENCES `tweet` (`id`),
  FOREIGN KEY (`id_retweeted`) REFERENCES `tweet` (`id`));

CREATE TABLE IF NOT EXISTS `reply` (
  `id_replier` BIGINT NOT NULL,
  `id_replied` BIGINT NOT NULL,
  PRIMARY KEY (`id_replier`, `id_replied`),
  FOREIGN KEY (`id_replier`) REFERENCES `tweet` (`id`),
  FOREIGN KEY (`id_replied`) REFERENCES `tweet` (`id`));

CREATE TABLE IF NOT EXISTS `quote` (
  `id_quoter` BIGINT NOT NULL,
  `id_quoted` BIGINT NOT NULL,
  PRIMARY KEY (`id_quoter`, `id_quoted`),
  FOREIGN KEY (`id_quoter`) REFERENCES `tweet` (`id`),
  FOREIGN KEY (`id_quoted`) REFERENCES `tweet` (`id`));

CREATE TABLE IF NOT EXISTS `follow` (
  `id_follower` BIGINT NOT NULL,
  `id_followed` BIGINT NOT NULL,
  PRIMARY KEY (`id_follower`, `id_followed`),
  FOREIGN KEY (`id_follower`) REFERENCES `account` (`id`),
  FOREIGN KEY (`id_followed`) REFERENCES `account` (`id`));

CREATE TABLE IF NOT EXISTS `mentions` (
  `mentioner` VARCHAR(15) NOT NULL,
  `mentioned` VARCHAR(15) NOT NULL,
  `created_at` DATE NULL,
  `tweet_id` BIGINT NULL,
  PRIMARY KEY (`mentioner`, `mentioned`));

CREATE INDEX `idx_tweet_id`  ON `twitter`.`tweet` (id);
CREATE INDEX `idx_account_id`  ON `twitter`.`account` (id);
CREATE INDEX `idx_created_at`  ON `twitter`.`tweet` (created_at) USING BTREE;

ALTER DATABASE twitter CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE tweet CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tweet CHANGE text text VARCHAR(560) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE account CHANGE description description VARCHAR(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;