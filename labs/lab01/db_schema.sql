-- MySQL Script generated by MySQL Workbench
-- sáb 27 fev 2021 15:56:05
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema medical_exams
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `medical_exams` ;

-- -----------------------------------------------------
-- Schema medical_exams
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `medical_exams` ;
USE `medical_exams` ;

-- -----------------------------------------------------
-- Table `medical_exams`.`requests`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `medical_exams`.`requests` ;

CREATE TABLE IF NOT EXISTS `medical_exams`.`requests` (
  `number` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `hour` TIME NOT NULL,
  `patient_id` INT NOT NULL,
  `patient_name` VARCHAR(100) NOT NULL,
  `patient_address` VARCHAR(250) NOT NULL,
  `patient_phone_number` VARCHAR(15) NOT NULL,
  `episode_number` INT NOT NULL,
  `report` LONGTEXT NULL,
  `status` VARCHAR(100) NOT NULL DEFAULT 'to be executed',
  `info` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`number`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medical_exams`.`work_list`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `medical_exams`.`work_list` ;

CREATE TABLE IF NOT EXISTS `medical_exams`.`work_list` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `request_num` INT NOT NULL,
  `done` TINYINT NOT NULL,
  `action` ENUM('create', 'edit', 'delete') NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_work_list_1_idx` (`request_num` ASC) VISIBLE,
  CONSTRAINT `fk_work_list_1`
    FOREIGN KEY (`request_num`)
    REFERENCES `medical_exams`.`requests` (`number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
