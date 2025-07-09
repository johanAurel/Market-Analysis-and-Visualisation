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
  instance_names = [
     "algo-trading-0",
    "algo-trading-1",
    "algo-trading-2",
     "algo-trading-3",
    "algo-trading-4",
    "algo-trading-5"
  ]  
}
