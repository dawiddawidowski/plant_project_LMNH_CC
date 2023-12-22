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

# Logging messages
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

# ECR Repository for Lambda Docker image
resource "aws_ecr_repository" "lambda_ecr_repo" {
  name = "c9-beetle-lambda-repo-terraform"
}

# IAM role to execute the Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "c9-beetle-lambda-role-terraform"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
    }]
  })
}

# Policies to attach to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_exec_policy_attachment" {
  role = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}

resource "aws_iam_role_policy_attachment" "s3_full_access_policy_attachment" {
  role = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "rds_full_access_policy_attachment" {
  role = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
}


# S3 bucket to store csv files containing database data
resource "aws_s3_bucket" "s3_bucket_terraform" {
  bucket = "c9-beetle-lmnh-plant-data-terraform"
}

# Lambda function to move database data into s3
resource "aws_lambda_function" "my_lambda" {
  function_name = "c9-beetle-lambda-terraform"
  role = aws_iam_role.lambda_role.arn

  # Image currently in existing non-terraform ECR repository
  image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-beetle-lambda-repo-terraform:latest"
  package_type = "Image"
  memory_size = 512
  timeout = 30

  environment {
    variables = {
      DB_HOST = var.DB_HOST
      DB_PASSWORD = var.DB_PASSWORD
      DB_USER = var.DB_USER
      DB_SCHEMA = var.DB_SCHEMA
      DB_NAME = var.DB_NAME
      DB_PORT = var.DB_PORT
      AKI = var.AKI
      SAK = var.SAK

    }
  }
}

# Displays name of Lambda function once Terraform applies the configuration
output "c9-beetle-lambda-terraform" {
  value = aws_lambda_function.my_lambda.function_name
}


# Event rule for each day
resource "aws_cloudwatch_event_rule" "daily_schedule" {
  name = "c9-beetle-daily-lambda-schedule-terraform"
  description = "Targets lambda function moving data to s3 once a day."
  schedule_expression = "cron(0 0 * * ? *)"
}

# Associate above rule with the Lambda
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule = aws_cloudwatch_event_rule.daily_schedule.name
  target_id = "TargetFunction"
  arn = aws_lambda_function.my_lambda.arn
}


# Give permission for EventBridge to invoke Lambda
resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.daily_schedule.arn
}

