# Terraform AWS Data Lake Configuration

This directory contains Terraform configuration for setting up an AWS data lake with S3 bucket suitable for AWS Glue.

## Project Structure

- `provider.tf` - AWS provider configuration and default tags
- `main.tf` - S3 bucket resource with versioning, encryption, and security settings
- `variables.tf` - Input variables for configuration
- `outputs.tf` - Output values (bucket ID, ARN, region)
- `terraform.tfvars.example` - Example variables file (copy and customize)
- `.gitignore` - Git ignore rules for Terraform files

## Prerequisites

1. **AWS Account**: You need valid AWS credentials configured
2. **Terraform**: Install Terraform >= 1.0
3. **AWS CLI**: Optional but recommended for credential management

### Configure AWS Credentials

```bash
# Option 1: Configure using aws-cli
aws configure

# Option 2: Set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

## Getting Started

1. **Copy the example variables file**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Edit terraform.tfvars** with your values:
   ```hcl
   aws_region   = "us-east-1"
   environment  = "dev"
   bucket_name  = "my-unique-bucket-name"  # Must be globally unique!
   project_name = "data-lake"
   ```
   
   ⚠️ **Important**: S3 bucket names must be globally unique across all AWS accounts!

3. **Initialize Terraform**:
   ```bash
   terraform init
   ```

4. **Review the plan**:
   ```bash
   terraform plan
   ```

5. **Apply the configuration**:
   ```bash
   terraform apply
   ```

## S3 Bucket Features

The Terraform configuration creates an S3 bucket with:

- **Versioning**: Enabled for data protection
- **Encryption**: Server-side encryption with AES256
- **Access Control**: Public access blocked
- **Tags**: Configured for Glue integration
- **Default Tags**: Automatically applied to all resources

## Next Steps

After creating the S3 bucket, you can expand this configuration to include:

- AWS Glue Catalog Database
- Glue Jobs for ETL workflows
- IAM roles and policies for Glue
- Lambda functions for data processing
- CloudWatch monitoring

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

## Troubleshooting

### Bucket name already exists
S3 bucket names must be globally unique. Try adding a suffix:
```hcl
bucket_name = "my-data-lake-bucket-${terraform.workspace}"
```

### Access Denied errors
Ensure your AWS credentials have permissions for:
- `s3:CreateBucket`
- `s3:PutBucketVersioning`
- `s3:PutBucketPublicAccessBlock`
- `s3:PutEncryptionConfiguration`

## References

- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [Terraform State Management](https://www.terraform.io/docs/language/state/)
