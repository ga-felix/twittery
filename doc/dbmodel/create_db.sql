CREATE SCHEMA IF NOT EXISTS `twitterDB` DEFAULT CHARACTER SET utf8mb4;
USE `twitterDB` ;

CREATE TABLE IF NOT EXISTS `tweet` (
  `id` BIGINT NOT NULL,
  `text` VARCHAR(560) NULL,
  `created_at` DATE NULL,
  `author_id` BIGINT NULL,
  `like_count` INT NULL,
  `retweet_count` INT NULL,
  `reply_count` INT NULL,
  `quote_count` INT NULL,
  `retweet_of` BIGINT NULL,
  `reply_of` BIGINT NULL,
  `quote_of` BIGINT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `account` (
  `id` BIGINT NOT NULL,
  `username` VARCHAR(15) NULL,
  `description` VARCHAR(720) NULL,
  `followers_count` INT NULL,
  `following_count` INT NULL,
  `tweet_count` INT NULL,
  `listed_count` INT NULL,
  `verified` TINYINT NULL,
  `created_at` DATE NULL,
  PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `account_follows` (
  `id_follower` BIGINT NOT NULL,
  `id_followed` BIGINT NOT NULL,
  PRIMARY KEY (`id_follower`, `id_followed`));

CREATE INDEX `idx_tweet_id`  ON `twitterDB`.`tweet` (id);
CREATE INDEX `idx_tweet_text`  ON `twitterDB`.`tweet` (text);
CREATE INDEX `idx_account_id`  ON `twitterDB`.`account` (id);
CREATE INDEX `idx_account_follows_id_follower`  ON `twitterDB`.`account_follows` (id_follower);
CREATE INDEX `idx_account_follows_id_followed`  ON `twitterDB`.`account_follows` (id_followed);
CREATE INDEX `idx_created_at`  ON `twitterDB`.`tweet` (created_at) USING BTREE;

ALTER DATABASE twitterDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE tweet CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tweet CHANGE text text VARCHAR(560) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE account CHANGE description description VARCHAR(720) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;