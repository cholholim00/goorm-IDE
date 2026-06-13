import sqlite3
from neo4j import GraphDatabase

# 1. Neo4j 연결 정보 (사용자 환경에 맞게 수정 필요)
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "qse789632145!"

class Migrator:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.conn = sqlite3.connect('student information database.db')
        self.cursor = self.conn.cursor()

    def close(self):
        self.driver.close()
        self.conn.close()

    def migrate(self):
        with self.driver.session() as session:
            # --- [Step 1] 기존 데이터 삭제 (초기화) ---
            session.run("MATCH (n) DETACH DELETE n")

            # --- [Step 2] Departments 테이블 -> Node 리팩토링 ---
            self.cursor.execute("SELECT * FROM Departments")
            for row in self.cursor.fetchall():
                session.run("""
                    CREATE (:Department {dept_id: $id, name: $name, office: $loc})
                """, id=row[0], name=row[1], loc=row[2])

            # --- [Step 3] Students 테이블 -> Node + 소속 관계 리팩토링 ---
            self.cursor.execute("SELECT * FROM Students")
            for row in self.cursor.fetchall():
                # 학생 노드 생성 및 학과(dept_id)와 즉시 연결
                session.run("""
                    MATCH (d:Department {dept_id: $dept_id})
                    CREATE (s:Student {id: $id, name: $name, email: $email, phone: $phone})
                    CREATE (s)-[:BELONGS_TO]->(d)
                """, id=row[0], name=row[1], email=row[2], phone=row[3], dept_id=row[4])

            # --- [Step 4] Courses 테이블 -> Node 리팩토링 ---
            self.cursor.execute("SELECT * FROM Courses")
            for row in self.cursor.fetchall():
                session.run("""
                    CREATE (:Course {course_id: $id, name: $name, credits: $credits, prof: $prof})
                """, id=row[0], name=row[1], credits=row[2], prof=row[3])

            # --- [Step 5] Enrollments 테이블 -> Relationship 리팩토링 (핵심!) ---
            self.cursor.execute("SELECT * FROM Enrollments")
            for row in self.cursor.fetchall():
                # 중간 테이블을 없애고 학생과 강의를 직접 연결
                session.run("""
                    MATCH (s:Student {id: $sid}), (c:Course {course_id: $cid})
                    CREATE (s)-[:ENROLLED_IN {grade: $grade, semester: $sem}]->(c)
                """, sid=row[1], cid=row[2], grade=row[3], sem=row[4])

        print("✅ 리팩토링 및 데이터 마이그레이션 완료!")

if __name__ == "__main__":
    migrator = Migrator()
    migrator.migrate()
    migrator.close()