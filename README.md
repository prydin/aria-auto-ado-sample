# Sample Aria Automation -> Azure Devops integration

A simple custom resource demonstrating how Azure Devops pipelines can be integrated with
Aria Automation. This example assumes Azure Devops is used to create some kind of resource and
two pipelines are used: One for creation and one for deletion. 

This is an example of a cloud template using this Custom Resource:

```yaml
formatVersion: 1
inputs:
  p1:
    type: string
    title: Param 1
    default: p1
  p2:
    type: string
    title: Param 2
    default: p2
resources:
  Custom_ADOPipeline_1:
    type: Custom.ADOPipeline
    properties:
      org: prydin
      project: terraform-poc
      variables: 
        var1: "hello"
        var2: "goodbye"
      parameters:
        p1: ${input.p1}
        p2: ${input.p2}
      creationPipeline: Terraform Apply
      deletionPipeline: Terraform Destroy
```

A few things are of interest here. First, notice the references to `creationPipeline` and `deletionPipeline`. 
Those are references by name to creation and deletion pipelines that will execute in response to the Create
and Destroy events respectively.

Also notice the `parameters` and `variables` sections. They can be used to pass arbitrary key/value pairs
as variables and parameters to the pipeline.

## Building the plugin

### Prerequisites
* Maven 3.8.4 or higher
* Docker running on the machine building the plugin

1. Clone or download the code
2. Change directory into the root of the code tree
3. Type: `mvn package`. The build should not result in any errors.
4. Verify that there's a file named `ado-plugin-<version>.zip` in the `target` directory.

### Installing the plugin
1. In Assembler/Cloud Assembly, navigate to Extensibility->Actions.
2. Click "Import"
3. Navigate to the `ado-plugin-<version>.zip` in the `target` directory.
4. Select a project and click on "Import"
5. Navigate to Design->Custom resources
6. Create a new custom resource called `ADOPipeline`. 
7. Map Create, Read and Destroy to the respective ADO-* actions you just imported.
8. Switch to the property tab and paste in the contents of the `schemas/ado-plugin.yaml` file in this source directory.
9. Create a secret called `ado_pat` and enter the Personal Access Token for the ADO service account you wish to use.
10. Navigate to Extensibility->Actions and edit the three "ADO-*" actions and replace the `ado_pat` variable with a reference to the secret you just created.

The plugin should now be ready to use!

*DISCLAIMER: This is sample code and not suitable for production use. I or any entity I'm associated with 
does not take any responsibility for damages caused by the use of this code. It is merely for demonstration
and educational purposes.*