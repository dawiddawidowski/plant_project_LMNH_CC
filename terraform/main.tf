provider "aws" {
  region = "eu-west-2"
}

# ECR Repository for pipeline Docker image
resource "aws_ecr_repository" "pipeline_ecr_repo" {
  name = "c9-beetle-pipeline-repo-terraform"
}

# Existing cohort 9 cluster, here for reference
data "aws_ecs_cluster" "existing_cluster" {
  cluster_name = "c9-ecs-cluster"
}

# My account for reference
data "aws_caller_identity" "current" {}

resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name = "beetle-log"
}

# Task definition for pipeline service
resource "aws_ecs_task_definition" "pipeline_task_def" {
  family = "c9-beetle-pipeline-task-def-terraform"
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = 1024
  memory = 3072
  execution_role_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/ecsTaskExecutionRole"
  container_definitions = jsonencode([{
    name = "c9-beetle-container"
    image = "${aws_ecr_repository.pipeline_ecr_repo.repository_url}"
    essential = true
    logConfiguration = {
    logDriver = "awslogs"
    options = {
        awslogs-group = aws_cloudwatch_log_group.ecs_log_group.name
        awslogs-region = "eu-west-2"
        awslogs-stream-prefix = "ecs"
      }
      }
    environment = [
      {
        name = "DB_USER"
        value = var.DB_USER
      },
      {
        name = "DB_PASSWORD"
        value = var.DB_PASSWORD
      },
      {
        name = "DB_HOST"
        value = var.DB_HOST
      }
    ]
    portMappings = [
      {
        name = "c9-beetle-container-80-tcp",
        containerPort = 80,
        hostPort = 80,
        protocol = "tcp",
        appProtocol = "http"
      }
    ]
  }])
}

# Pipeline service associated with the task definition
resource "aws_ecs_service" "pipeline_service" {
  name = "c9-beetle-pipeline-service-terraform"
  cluster = data.aws_ecs_cluster.existing_cluster.id
  task_definition = aws_ecs_task_definition.pipeline_task_def.arn
  launch_type = "FARGATE"
  network_configuration {
    subnets = ["subnet-02a00c7be52b00368",
              "subnet-0d0b16e76e68cf51b",
              "subnet-081c7c419697dec52"]
    security_groups = ["sg-020697b6514174b72"]
    assign_public_ip = true
  }
  desired_count = 1  
}
