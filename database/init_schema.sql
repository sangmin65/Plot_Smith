물론입니다! 작가님의 세계관과 설정을 완벽하게 통제하고 무결성을 지켜줄 MySQL 데이터베이스 생성 스크립트(DDL)를 바로 짜드리겠습니다.

설계해 드린 스키마를 바탕으로, 외래키(Foreign Key) 제약 조건과 상태를 강제하는 ENUM 타입, 그리고 유연성을 위한 JSON 타입까지 모두 적용한 실무용 코드입니다.

MySQL Workbench나 DBeaver 같은 DB 툴, 혹은 터미널 창에 아래 코드를 그대로 복사해서 실행하시면 됩니다.

🗄️ Plot_Smith v2.0 DB 생성 SQL 스크립트
SQL
-- 1. 데이터베이스 생성 및 한글 깨짐 방지 세팅
CREATE DATABASE IF NOT EXISTS plot_smith DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE plot_smith;

-- 2. Projects (작품 테이블)
CREATE TABLE IF NOT EXISTS Projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- 작성자 ID (추후 유저 테이블과 연동)
    title VARCHAR(255) NOT NULL,
    synopsis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Characters (등장인물 테이블)
CREATE TABLE IF NOT EXISTS Characters (
    char_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    status ENUM('ALIVE', 'DEAD', 'MISSING', 'SEALED') DEFAULT 'ALIVE', -- 상태 제약 조건
    current_location VARCHAR(255),
    attributes JSON, -- 소지금, 체력 등 유연한 스탯 관리를 위한 JSON
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE
);

-- 4. World_Wiki (세계관 규칙/설정 테이블)
CREATE TABLE IF NOT EXISTS World_Wiki (
    rule_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    category VARCHAR(50) NOT NULL, -- 예: GEOGRAPHY, MAGIC_SYSTEM, LAW
    key_term VARCHAR(100) NOT NULL, -- 예: 마력 고갈
    description TEXT,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE
);

-- 5. Chapters (회차별 원고 테이블)
CREATE TABLE IF NOT EXISTS Chapters (
    chapter_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    chapter_number INT NOT NULL,
    title VARCHAR(255),
    content LONGTEXT NOT NULL,
    is_analyzed BOOLEAN DEFAULT FALSE, -- AI 검증을 거쳤는지 확인하는 플래그
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE
);

-- 6. Validation_Logs (설정 충돌 검증 로그 테이블 - QA 리포트)
CREATE TABLE IF NOT EXISTS Validation_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    chapter_id INT NOT NULL,
    error_type ENUM('DEATH_VIOLATION', 'INVENTORY_OVERFLOW', 'TIMELINE_MISMATCH', 'RULE_VIOLATION') NOT NULL,
    message TEXT NOT NULL, -- 예: "12화에서 사망한 '김철수'가 15화 원고에 등장했습니다."
    is_resolved BOOLEAN DEFAULT FALSE, -- 작가가 오류를 수정했는지 여부
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (chapter_id) REFERENCES Chapters(chapter_id) ON DELETE CASCADE
);