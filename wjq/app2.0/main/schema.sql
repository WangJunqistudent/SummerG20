CREATE TABLE IF NOT EXISTS files (
  id INT PRIMARY KEY AUTO_INCREMENT,
  file_path VARCHAR(255) NOT NULL,
  line_number INT NOT NULL,
  line_text TEXT NOT NULL
);