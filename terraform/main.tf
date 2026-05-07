data "aws_ami" "ubuntu" {
  most_recent = true

  owners = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_security_group" "booking_sg" {
  name = "booking-platform-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "booking_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  key_name = "booking-platform"

  security_groups = [aws_security_group.booking_sg.name]

  user_data = <<-EOF
#!/bin/bash

exec > /var/log/user-data.log 2>&1
set -x

sleep 30

apt update -y

apt install -y docker.io git curl

systemctl start docker
systemctl enable docker

usermod -aG docker ubuntu

mkdir -p /usr/local/lib/docker/cli-plugins

curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
-o /usr/local/lib/docker/cli-plugins/docker-compose

chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

ln -s /usr/local/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose || true

cd /home/ubuntu

until git clone https://github.com/myadavg/Booking-platform.git
do
  echo "Retrying git clone..."
  sleep 5
done

cd Booking-platform

cat > .env <<EOT
DATABASE_URL=postgresql://postgres:postgres@db:5432/bookingdb
APP_ENV=dev
APP_NAME=Booking Platform
LOG_LEVEL=INFO
EOT

docker compose up -d --build

EOF

  tags = {
    Name = "booking-platform-terraform"
  }
}
