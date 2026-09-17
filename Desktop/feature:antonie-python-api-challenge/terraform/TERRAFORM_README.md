# Terraform Infrastructure Setup - Books API

This directory contains the Infrastructure as Code (IaC) for deploying the Books API to AWS. The setup creates a production-ready, scalable, and secure infrastructure using AWS services.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [File Descriptions](#file-descriptions)
- [Deploying to AWS](#deploying-to-aws)
- [Monitoring](#monitoring)
- [Costs](#costs)
- [Cleanup](#cleanup)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The Terraform configuration creates the following AWS infrastructure:

### Container Hosting
- **Amazon ECS Fargate**: Serverless container orchestration platform
  - Automatically scales between 2-4 tasks based on CPU/memory metrics
  - No server management required
  - Pay only for resources used

### Load Balancing
- **Application Load Balancer (ALB)**: Distributes incoming traffic
  - Listens on HTTP (80) and HTTPS (443)
  - Routes traffic to ECS tasks
  - Health checks every 30 seconds

### Database
- **Amazon DocumentDB**: MongoDB-compatible database service
  - Fully managed with automatic backups
  - Multi-AZ deployment for high availability
  - Encryption at rest with KMS
  - Supports 2-3 instances for redundancy

### Networking
- **VPC** with public and private subnets across 3 availability zones
- **NAT Gateways** for private subnet internet access
- **Security Groups** for fine-grained network access control
- **Route Tables** for traffic routing

### Monitoring & Logging
- **CloudWatch Logs**: Application logs stored centrally
- **CloudWatch Alarms**: Alerts for CPU, memory, and database metrics
- **CloudWatch Metrics**: Monitor resource utilization

### Security
- **AWS KMS**: Encryption for DocumentDB
- **IAM Roles**: Least privilege access for ECS tasks
- **Security Groups**: Network-level access control
- **Private Subnets**: Database runs in isolated network

## Prerequisites

### Required Software
```bash
# Terraform (version 1.0 or later)
terraform --version

# AWS CLI (version 2.0 or later)
aws --version

# Docker (for building images)
docker --version
```

### AWS Account Setup
1. Create an AWS account or use existing one
2. Create an IAM user with programmatic access
3. Attach policies:
   - `AmazonECS_FullAccess`
   - `AmazonDocDBServiceRolePolicy`
   - `AmazonVPCFullAccess`
   - `AmazonEC2FullAccess`
   - `CloudWatchLogsFullAccess`
   - `IAMFullAccess`
   - `KMSFullAccess`

### AWS Credentials
```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Docker Image
You need to push your Docker image to ECR:

```bash
# Create ECR repository
aws ecr create-repository --repository-name books-api --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com

# Build and push image
docker build -t books-api:latest .
docker tag books-api:latest [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/books-api:latest
docker push [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/books-api:latest
```

## Quick Start

### 1. Initialize Terraform

```bash
cd terraform

# Download Terraform modules and plugins
terraform init

# Output:
# Terraform has been successfully configured!
```

### 2. Create Configuration File

```bash
# Copy example configuration
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
nano terraform.tfvars
```

### 3. Review the Plan

```bash
# See what Terraform will create
terraform plan -out=tfplan

# Output shows all resources to be created
```

### 4. Apply Configuration

```bash
# Create AWS resources
terraform apply tfplan

# Wait 10-15 minutes for all resources to be created
```

### 5. Get API URL

```bash
# Display outputs
terraform output

# Example output:
# alb_dns_name = "books-api-alb-123456.us-east-1.elb.amazonaws.com"
# api_url = "http://books-api-alb-123456.us-east-1.elb.amazonaws.com"
```

## Configuration

### terraform.tfvars

Copy `terraform.tfvars.example` and customize:

```hcl
# AWS Configuration
aws_region = "us-east-1"
environment = "production"
project_name = "books-api"

# VPC Configuration
vpc_cidr = "10.0.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

# ECS Configuration
ecs_desired_count = 2        # Number of running tasks
ecs_max_capacity = 4         # Maximum for auto-scaling
ecs_task_cpu = "256"         # 0.25 CPU
ecs_task_memory = "512"      # 512 MB RAM

# Database Configuration
db_instance_count = 2        # Number of DocumentDB nodes
db_instance_class = "db.t4g.medium"
db_backup_retention_days = 7
db_username = "admin"
db_password = "YourSecurePassword123!"

# Container Image
ecr_repository_url = "123456789012.dkr.ecr.us-east-1.amazonaws.com/books-api"
docker_image_tag = "latest"
```

### Key Variables Explained

| Variable | Purpose | Recommended Value |
|----------|---------|-------------------|
| `aws_region` | AWS region to deploy to | `us-east-1` |
| `vpc_cidr` | VPC network range | `10.0.0.0/16` |
| `ecs_task_cpu` | CPU per container | `256` (0.25 vCPU) |
| `ecs_task_memory` | Memory per container | `512` MB |
| `ecs_desired_count` | Running containers | `2` (min for HA) |
| `ecs_max_capacity` | Max containers | `4` |
| `db_instance_class` | Database size | `db.t4g.medium` |
| `db_instance_count` | Database replicas | `2` (min for HA) |

## File Descriptions

### main.tf
Main Terraform configuration file containing:
- **VPC & Network**: VPC, subnets, route tables, NAT gateways
- **Security Groups**: Network access rules for ALB, ECS, and RDS
- **Application Load Balancer**: Traffic distribution and health checks
- **ECS Cluster**: Container orchestration setup
- **ECS Task Definition**: Container image, CPU, memory, environment variables
- **ECS Service**: Service configuration and load balancer integration
- **Auto Scaling**: CPU and memory-based scaling policies
- **DocumentDB**: MongoDB-compatible database cluster
- **CloudWatch**: Logs and alarms for monitoring
- **KMS**: Encryption key for database

### variables.tf
Terraform input variables with:
- Default values (customizable)
- Type constraints
- Descriptions
- Sensitive flag for passwords

### outputs.tf
Terraform outputs providing:
- ALB DNS name
- ECS cluster information
- DocumentDB connection details
- CloudWatch log group
- API URLs (HTTP and docs)

### terraform.tfvars.example
Template for configuration values:
- VPC CIDR and subnets
- ECS task specifications
- Database credentials and sizing
- Container image location

## Deploying to AWS

### Step-by-Step Deployment

#### 1. Prepare Docker Image

```bash
# Build image locally
docker build -t books-api:latest ..

# Create ECR repository (if not exists)
aws ecr create-repository \
  --repository-name books-api \
  --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag books-api:latest \
  [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/books-api:latest

# Push to ECR
docker push \
  [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/books-api:latest
```

#### 2. Initialize Terraform

```bash
cd terraform
terraform init

# Backend configuration (optional, for state management)
# Uncomment backend block in main.tf and configure S3 bucket
```

#### 3. Create Configuration

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
nano terraform.tfvars
```

#### 4. Plan Deployment

```bash
terraform plan -out=tfplan

# Review all resources to be created
# Budget estimation available in AWS Pricing Calculator
```

#### 5. Apply Configuration

```bash
terraform apply tfplan

# Terraform will:
# 1. Create VPC and networking (2-3 minutes)
# 2. Set up ALB (2-3 minutes)
# 3. Create ECS cluster and service (1-2 minutes)
# 4. Provision DocumentDB (8-10 minutes) ← Longest step
# 5. Set up monitoring (1 minute)

# Total time: ~15-20 minutes
```

#### 6. Verify Deployment

```bash
# Get API URL
terraform output api_url

# Wait for ALB to register targets
aws elbv2 describe-target-health \
  --target-group-arn $(terraform output -raw target_group_arn) \
  --region us-east-1

# Test API
curl $(terraform output -raw api_url)/health
curl $(terraform output -raw api_docs_url)
```

## Monitoring

### CloudWatch Logs

View application logs:
```bash
# Get log group name
terraform output cloudwatch_log_group

# View logs
aws logs tail /ecs/books-api --follow

# Filter by error
aws logs filter-log-events \
  --log-group-name /ecs/books-api \
  --filter-pattern "ERROR"
```

### CloudWatch Alarms

Automatically created alarms:
- **ECS CPU High**: Triggers when CPU > 80%
- **ECS Memory High**: Triggers when memory > 85%
- **DocumentDB CPU High**: Triggers when CPU > 75%

View alarms:
```bash
aws cloudwatch describe-alarms \
  --region us-east-1
```

### ECS Service

Check service status:
```bash
# Get cluster name
CLUSTER=$(terraform output -raw ecs_cluster_name)

# Get service name
SERVICE=$(terraform output -raw ecs_service_name)

# Describe service
aws ecs describe-services \
  --cluster $CLUSTER \
  --services $SERVICE \
  --region us-east-1
```

### Database Health

```bash
# Get cluster endpoint
ENDPOINT=$(terraform output -raw docdb_cluster_endpoint)

# Monitor cluster
aws docdb describe-db-clusters \
  --db-cluster-identifier $(terraform output -raw docdb_cluster_name) \
  --region us-east-1
```

## Costs

### Estimated Monthly Costs (for recommended configuration)

| Service | Component | Estimated Cost |
|---------|-----------|-----------------|
| **ECS Fargate** | 2 vCPU + 4GB RAM per task, 2 tasks | ~$60/month |
| **DocumentDB** | 2x db.t4g.medium instances | ~$150/month |
| **Application Load Balancer** | ALB + data processing | ~$20/month |
| **NAT Gateway** | Data transfer | ~$30/month |
| **CloudWatch** | Logs + alarms | ~$10/month |
| **Data Transfer** | Out of region | ~$15/month |
| **Total Estimate** | | ~**$285/month** |

### Cost Optimization Tips

1. **Reduce instances**: Use `ecs_desired_count = 1` for dev environments
2. **Smaller database**: Use `db.t4g.small` for lower traffic
3. **Reserved Capacity**: Purchase 1-year commitments for 30-40% savings
4. **Spot Instances**: Use Fargate Spot for non-critical workloads
5. **Data Transfer**: Minimize data transfer between regions

## Cleanup

### Remove All AWS Resources

```bash
cd terraform

# Destroy all resources
terraform destroy

# When prompted, type "yes" to confirm

# Verify resources are deleted
aws ec2 describe-instances --region us-east-1
```

### Partial Cleanup

```bash
# Remove specific resources
terraform destroy -target=aws_ecs_service.app

# Destroy and skip final snapshot
terraform destroy -auto-approve \
  -var="skip_final_snapshot=true"
```

## Troubleshooting

### Terraform Init Fails

**Error**: "required_providers: conflicting requirements"

**Solution**: Upgrade Terraform
```bash
terraform -version
# Should be 1.0 or later

# Upgrade on macOS
brew upgrade terraform

# Or download from https://www.terraform.io/downloads
```

### ECS Tasks Not Starting

**Error**: "CannotPullContainerImage" in ECS events

**Solution**: Verify Docker image
```bash
# Check image exists in ECR
aws ecr list-images --repository-name books-api

# Check ECR credentials in ECS task role
# Ensure task role has access to ECR

# Re-push image
docker push [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/books-api:latest

# Force service update
aws ecs update-service \
  --cluster books-api-cluster \
  --service books-api-service \
  --force-new-deployment
```

### Database Connection Issues

**Error**: "Unable to connect to DocumentDB"

**Solution**: Check security groups
```bash
# List security group rules
aws ec2 describe-security-groups \
  --filter Name=group-name,Values=books-api-rds-sg

# Ensure port 27017 is open from ECS security group
# Check network connectivity from ECS task
aws ecs execute-command \
  --cluster books-api-cluster \
  --task [TASK_ID] \
  --interactive \
  --command "/bin/bash"
```

### High Costs

**Error**: Unexpected high AWS bill

**Solution**: Review resources
```bash
# Get all resource costs
terraform plan | grep -E "^  (aws_|~)"

# Identify expensive resources
# Compare with AWS Cost Explorer console
# Consider reducing instance counts or sizes
```

### State File Issues

**Error**: "state lock" or "Backend initialization required"

**Solution**: Check state management
```bash
# List local state
terraform state list

# Show specific resource
terraform state show aws_ecs_service.app

# If using remote state, force unlock
terraform force-unlock LOCK_ID
```

## Advanced Topics

### Using Remote State

Store Terraform state in S3 for team collaboration:

```hcl
# In main.tf, uncomment backend block
backend "s3" {
  bucket         = "my-terraform-state"
  key            = "books-api/terraform.tfstate"
  region         = "us-east-1"
  encrypt        = true
  dynamodb_table = "terraform-locks"
}
```

```bash
# Create S3 bucket and DynamoDB table first
aws s3 mb s3://my-terraform-state
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Reconfigure backend
terraform init
```

### HTTPS with ACM

Add SSL certificate:

```hcl
# Create certificate
resource "aws_acm_certificate" "main" {
  domain_name       = "api.example.com"
  validation_method = "DNS"
}

# Add HTTPS listener to ALB
# Update security group to allow 443
```

### Custom Domain

```bash
# Create Route53 record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456 \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "api.example.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z1234",
          "DNSName": "books-api-alb-123.us-east-1.elb.amazonaws.com",
          "EvaluateTargetHealth": false
        }
      }
    }]
  }'
```

## Support

For issues or questions:

1. **Terraform Docs**: https://www.terraform.io/docs/
2. **AWS Terraform Provider**: https://registry.terraform.io/providers/hashicorp/aws/latest
3. **AWS Documentation**: https://docs.aws.amazon.com/
4. **Terraform Cloud**: https://app.terraform.io/ (free tier available)

---

**Last Updated**: 2024-01-16  
**Terraform Version**: >= 1.0  
**AWS Provider Version**: >= 5.0
