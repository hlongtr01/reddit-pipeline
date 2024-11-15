provider "aws" {
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
    region = var.aws_region
}

resource "aws_security_group" "rds_security" {
    name_prefix = "rds_security_group"
    ingress {
        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_db_instance" "rds_postgres" {
    engine = "postgres"
    engine_version = "14.13"
    db_name = "reddit"
    identifier = "reddit"
    instance_class = "db.t3.micro"
    allocated_storage = 10
    publicly_accessible = true
    username = var.rds_username
    password = var.rds_password
    vpc_security_group_ids = [aws_security_group.rds_security.id]
    skip_final_snapshot = true
    tags = {
        Name = "reddit-database"
    }
}