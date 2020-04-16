CREATE DATABASES epytodo;

CREATE TABLE user (
    user_id INT NOT NULL AUTO_INCREMENT,
    username varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE task (
    task_id INT NOT NULL AUTO_INCREMENT,
    title varchar(100) NOT NULL,
    begin TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end TIMESTAMP DEFAULT 0,
    status ENUM('not started', 'in progress', 'done') DEFAULT 'not started',
    creator varchar(100) DEFAULT NULL,
    PRIMARY KEY (task_id)
);

CREATE TABLE user_has_task (
    fk_user_id INT NOT NULL,
    fk_task_id INT NOT NULL,
    PRIMARY KEY (fk_user_id)
);