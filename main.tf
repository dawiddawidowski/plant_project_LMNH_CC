provider "aws" {
  region = "eu-west-2"
}

# ECR Repository for pipeline Docker image
resource "aws_ecr_repository" "pipeline_ecr_repo" {
  name = "c9-beetle-pipeline-repo"
}

# Existing cohort 9 cluster, here for reference
data "aws_ecs_cluster" "existing_cluster" {
  cluster_name = "c9-ecs-cluster"
}

# Task definition for pipeline service
resource "aws_ecs_task_definition" "pipeline_task_def" {
  family = "pipeline_task"
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = "1024"
  memory = "3072"
  execution_role_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  container_definitions = jsonencode([{
    name = "c9-beetle-container"
    image = "${aws_ecr_repository.pipeline_ecr_repo.repository_url}:latest"
    environment = [
      {
        name = "db_user"
        value = var.db_user
      },
      {
        name = "db_password"
        value = var.db_password
      },
      {
        name = "db_host"
        value = var.db_host
      }
    ]
  }])
}

# Pipeline service associated with the task definition
resource "aws_ecs_service" "pipeline_service" {
  name = "c9-beetle-pipeline-service"
  cluster = data.aws_ecs_cluster.existing_cluster.id
  task_definition = aws_ecs_task_definition.pipeline_task_def.arn
  launch_type = "FARGATE"
  network_configuration {
    subnets = ["subnet-02a00c7be52b00368", "subnet-0769b8ef4ea96e48d",
              "subnet-0d0b16e76e68cf51b", "subnet-01601bef1d13fed8a",
              "subnet-081c7c419697dec52", "subnet-003202ce735ee7a7d"]
  }
  desired_count = 1  
}