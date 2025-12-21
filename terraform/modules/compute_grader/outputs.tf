output "instance_name" {
  description = "The name of the grader analyzer compute instance"
  value       = google_compute_instance.grader_analyzer.name
}

output "instance_self_link" {
  description = "The self-link of the grader analyzer instance"
  value       = google_compute_instance.grader_analyzer.self_link
}
