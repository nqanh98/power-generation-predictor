CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS `pcs_units` (
  `id` bigint(20) PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `cc_name` varchar(30),
  `pp_name` varchar(30) NOT NULL,
  `data_url` varchar(255) DEFAULT NULL,
  `status` ENUM ('0', '1'),
  `last_update` datetime
);

CREATE TABLE IF NOT EXISTS `models` (
  `id` bigint(20) PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `framework` varchar(20) NOT NULL,
  `pcs_unit_id` bigint(20) NOT NULL,
  `model_url` varchar(255) DEFAULT NULL,
  `status` ENUM ('draft', 'training', 'completed', 'published', 'failed', 'aborted'),
  `project_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT (now())
);

CREATE TABLE IF NOT EXISTS `projects` (
  `id` bigint(20) PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `owner` bigint(20) NOT NULL,
  `status` ENUM ('pending', 'running', 'completed', 'failed', 'aborted'),
  `start_date` datetime DEFAULT (now()),
  `end_date` datetime
);

ALTER TABLE `models` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

ALTER TABLE `projects` ADD FOREIGN KEY (`owner`) REFERENCES `users` (`id`);

ALTER TABLE `models` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `models` ADD FOREIGN KEY (`pcs_unit_id`) REFERENCES `pcs_units` (`id`);

CREATE UNIQUE INDEX `users_index_0` ON `users` (`username`);

CREATE UNIQUE INDEX `users_index_1` ON `users` (`email`);
