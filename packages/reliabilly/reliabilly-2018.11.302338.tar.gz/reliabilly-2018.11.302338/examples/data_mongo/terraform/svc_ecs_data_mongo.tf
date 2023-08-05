variable "port_data_mongo" {
  default = 8000
}

module "ecs_service_data_mongo" {
  source = "./ecs_tasks/"

  name                  = "platform-data_mongo"
  environment           = "${var.environment}"
  container_definitions = "./container_definitions/svc_data_mongo.json"
  container_port        = "${var.port_data_mongo}"
  target_group_arn      = "${aws_lb_target_group.data_mongo.arn}"

  template_variables = {
    image        = "reliabilly/data_mongo"
    service_name = "data_mongo"
    image_tag    = "${var.release_number}"
    build_number = "${var.build_number}"
    environment  = "${var.environment}"
  }

  lb_arn          = "${aws_lb.lb.arn}"             # Used as a replacement for depends_on until module support is added
  lb_listener_arn = "${aws_lb_listener.https.arn}" # Used as a replacement for depends_on until module support is added
}

resource "aws_lb_target_group" "data_mongo" {
  name     = "reliabilly-${var.name}-data_mongo"
  port     = "${var.port_data_mongo}"
  protocol = "HTTP"
  vpc_id   = "${data.aws_vpc.shared_services.id}"

  health_check = {
    path = "/data_mongo/ping/"
  }

  depends_on = ["aws_lb.lb"]

  tags = "${var.aws_tags}"
}

resource "aws_lb_listener_rule" "data_mongo" {
  listener_arn = "${aws_lb_listener.https.arn}"

  action {
    type             = "forward"
    target_group_arn = "${aws_lb_target_group.data_mongo.arn}"
  }

  condition {
    field  = "path-pattern"
    values = ["/data_mongo/*"]
  }
}