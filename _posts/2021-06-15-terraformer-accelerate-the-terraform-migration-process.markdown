---
title: "Terraformer accelerates the Terraform migration process"
layout: post
date: 2021-06-15 10:21:54 +0900
image: 'assets/img/posts/2021-06-15-terraformer-accelerate-the-terraform-migration-process/catch.jpg'
description:
tag: ['Terraform', 'AWS']
blog: true
author: "Kai Sasaki"
---

Although infrastructure-as-code is an excellent concept we all should obey, migration of infrastructure set up to written code is always challenging. The final infrastructure should be identical to the existing one to avoid the wide range of [catastrophic failures](https://en.wikipedia.org/wiki/Catastrophic_failure). But manually writing the Terraform code (or any other infrastructure automation tool) is troublesome and error-prone. It can often force us to write and check much code to ensure it is consistent with the current infrastructure setup.

I found [Terraformer](https://github.com/GoogleCloudPlatform/terraformer) is helpful for this purpose. It automatically loads states and writes the initial HCL code as we can get started on it.


# [Terraformer](https://github.com/GoogleCloudPlatform/terraformer)

Terraformer provides two options, `import` and `plan`. `import` imports the current TF state and writes the HCL code for us. `plan` only loads the state and shows what type of resource it is going to create. We can run `plan` first as we use Terraform to check the result of the command will work as expected.

```bash
$ terraformer --help
Usage:
   [command]

Available Commands:
  help        Help about any command
  import      Import current state to Terraform configuration
  plan        Plan to import current state to Terraform configuration
  version     Print the version number of Terraformer

Flags:
  -h, --help      help for this command
  -v, --version   version for this command

Use " [command] --help" for more information about a command.
```

The following command will allow you to import AWS infrastructure.

```bash
$ terraformer plan aws
```

If you want to use the specific profile of the AWS role, we have a `--profile` option.

```bash
$ terraformer plan aws --profile <Your Profile>
```

Terraformer will dump the state file in the directory named `generated` as default. Next, you can generate the corresponding HCL code by the `import` command if the state looks okay.

```bash
$ terraformer import aws --profile <Your Profile>
```

One note is that it will create a brand-new infrastructure set, not modify the existing one. So please adjust the resource names as you like because all have prefixes `tfer--` and auto-generated identifiers. 