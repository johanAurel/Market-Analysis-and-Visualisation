provider "aws" {
  region = "eu-west-2"  # London
}
module "networking" {
  source = "./modules/vpc"
}

module "ec2_instance" {
  source            = "./modules/ec2"
  subnet_id         = module.networking.public_subnet_id
  security_group_id = module.networking.security_group_id
    # Create this in AWS EC2 dashboard first
 
}
