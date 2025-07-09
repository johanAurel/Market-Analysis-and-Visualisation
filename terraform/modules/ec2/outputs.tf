output "public_ips" {
  description = "List of public IPs of the EC2 instances"
  value       = [for instance in aws_instance.this : instance.public_ip]
}
