---
title: "How to add new policy to IAM role by Terraform"
layout: post
date: 2021-04-06 08:18:15 +0900
image: 'assets/img/posts/2021-04-06-how-to-add-new-policy-to-iam-role/catch.jpg'
description:
tag: ['Terraform', 'AWS', 'IAM', 'Security']
blog: true
author: "Kai Sasaki"
---

Security management in a fine-grained manner is a critical component to deploy the enterprise application successfully. [Terraform](https://www.terraform.io/) enables us to manage any resource on the cloud service by using the declarative language, [HCL](https://github.com/hashicorp/hcl/blob/main/hclsyntax/spec.md). If you are a software engineer providing any service on AWS like me, Terraform gives us the excellent capability and saves us time for sure. I have found a tiny tip to be shared here about the Terraform usage setting the IAM policy. This article aims to explain the use of `aws_iam_role_policy` and its potential limitations from the practical viewpoint.

# Limitation of `aws_iam_role_policy`

We used [`aws_iam_role_policy`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) to set the specific IAM policy to a role. It's the most straightforward and easy way to attach a policy to the role you are managing. But there is a caveat to be noted. The resource can only create **inline policy**, which is not designed to be shared by multiple roles afterward.

Looking at the following list, you can notice that the policy attached to `my-role` does not have any name specified. Even if the policy is sufficiently general to be used by other roles, we have no way with `aws_iam_role_policy`.

```tf
resource "aws_iam_role" "my-role" {
 name = "my-role"

 assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "my-policy" {
 name = "my-policy"
 role = "${aws_iam_role.my-role.id}"


 # This policy is exclusively available by my-role.
 policy = <<-EOF
 {
   "Version": "2012-10-17",
   "Statement": [
     {
       "Sid": "AccessObject",
       "Effect": "Allow",
       "Action": [
         "s3:GetObject"
       ],
      "Resource": [
        "arn:aws:s3:::my-bucket"
      ]
     }
   ]
 }
EOF
```

# Standalone policy with `aws_iam_policy`

Here comes the `aws_iam_policy` and `aws_iam_role_policy_attachment` resources. [`aws_iam_policy`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) is a resource to create a standalone IAM policy. It's almost the same as what `aws_iam_role_policy` does, but it does not attach the policy with any IAM entity such as users, roles, and groups. The policy is isolated and does not affect unless it is attached to the existing IAM entity. [`aws_iam_role_policy_attachment`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) does that as the name implied. You can attach the existing policy to the existing IAM role. That indicates we can reuse the policy by attaching it to several roles.

```tf
resource "aws_iam_policy" "my-policy" {
 name = "my-policy"

 policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AccessObject",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "my-policy-attach" {
  role = "${aws_iam_role.my-role.name}"
  policy_arn = "${aws_iam_policy.my-policy.arn}"
}
```

If you have another role named `my-role-2`, you can attach the `my-policy` again with the following code's call.

```tf
resource "aws_iam_role_policy_attachment" "my-policy-attach-2" {
  role = "${aws_iam_role.my-role-2.name}"
  policy_arn = "${aws_iam_policy.my-policy.arn}"
}
```

That's a handy way to reuse the existing policy component and be less error-prone because we can avoid rewriting the same policy repeatedly.


# WARNING

We have another resource that has a very similar name,
[`aws_iam_policy_attachment`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment). But we should be careful of the usage of this resource because it attaches the policy **exclusively**. Across the entire AWS account, only one IAM entity (i.e., users/roles/groups) can be declared by `aws_iam_policy_attachement`. That limitation is counterintuitive. Using `aws_iam_role_policy_attachment` will prevent us from wasting time digging deeper into what's going on when facing an issue.

# Reference

- [Difference between different policy resources, Reddit](https://www.reddit.com/r/Terraform/comments/fbts88/difference_between_different_policy_resources/)
- [aws_iam_role_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment)
- [aws_iam_role_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy)