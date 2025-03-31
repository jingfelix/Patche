from mcp.types import Prompt

from Patche.mcp.model import (
    PatcheApply,
    PatcheConfig,
    PatcheList,
    PatcheShow,
    PatcheTools,
)

base_info_prompt = """
<system>

You are a tool that helps the user to manage patches in a directory.

There are several tools available to you, you can use them to perform different actions.

When using a tool, you should call it with given arguments, and do not add any other information.

</system>
"""

show_config_prompt = f"""
<user>

Please show the configuration of the tool.

Parameters:
- config_path: string, path to the configuration file (optional)
- patche_dir: string, directory containing patches (required)

</user>

Please use the following format to show the configuration:

<input>
{PatcheConfig.model_json_schema()}
</input>
"""

list_prompt = f"""
<user>

Please list all the patches in the directory.

Parameters:
- patche_dir: string, directory path containing patches (required)

</user>

Please use the following format to show the patches:

<input>
{PatcheList.model_json_schema()}
</input>
"""

show_prompt = f"""
<user>

Please show infomation of the patch.

Parameters:
- patch_path: string, path to the patch file to display (required)

</user>

Please use the following format to show the patch:

<input>
{PatcheShow.model_json_schema()}
</input>
"""

apply_prompt = f"""
<user>

Please apply a patch to a target directory.

Parameters:
- patch_path: string, path to the patch file (required)
- target_dir: string, directory to apply the patch to (required)
- reverse: boolean, whether to reverse apply the patch (optional)

</user>

Please use the following format to apply the patch:

<input>
{PatcheApply.model_json_schema()}
</input>

The patch will be applied to the target directory. You can also set `reverse` to `true` to reverse the patch application.
"""

reverse_apply_prompt = f"""
<user>

Please reverse apply a patch to a target directory.

Parameters:
- patch_path: string, path to the patch file (required)
- target_dir: string, directory to reverse apply the patch to (required)
- reverse: boolean, default true for reverse application

</user>

Please use the following format to reverse apply the patch:

<input>
{{
  "patch_path": "Path to the patch file",
  "target_dir": "Path to the target directory",
  "reverse": true
}}
</input>

This will undo the changes made by the patch.
"""

help_prompt = """
<user>

Please show me how to use patche and what commands are available.

</user>

I can help you manage patches with Patche. Here are the available commands:

1. **Show Configuration**: View the current Patche configuration
   - Use `patche_config` tool

2. **List Patches**: See all available patches in a directory
   - Use `patche_list` tool with the directory path

3. **Show Patch Details**: View metadata and content of a specific patch
   - Use `patche_show` tool with the patch file path

4. **Apply Patch**: Apply a patch to a target directory
   - Use `patche_apply` tool with patch path and target directory
   - Add `"reverse": true` to undo a patch

Would you like me to help you with any of these operations?
"""

patch_creation_guidance_prompt = """
<user>

How can I create a new patch?

</user>

To create a new patch with Patche, you need to:

1. Make changes to your files that you want to include in the patch
2. Create a backup of the original files (e.g., by copying them with a `.orig` extension)
3. Use a command like `diff -u original_file modified_file > my_patch.patch` to generate the patch

If you're using the Patche CLI directly, you can use:
```
patche create --name "my-patch-name" --description "What this patch does" --files file1.py file2.py
```

The patch will be saved in your configured patches directory and can then be applied to other projects.

Would you like me to help you apply an existing patch instead?
"""

patche_workflow_prompt = """
<user>

Please explain the typical workflow for using Patche.

</user>

# Typical Patche Workflow

The standard workflow for using Patche involves:

1. **Create or obtain patches**
   - Create patches from modified files
   - Download or receive patches from others

2. **Manage your patch collection**
   - List available patches with `patche_list`
   - Examine patch details with `patche_show`

3. **Apply patches to projects**
   - Apply a patch with `patche_apply`
   - Specify target directory and patch path

4. **Revert changes if needed**
   - Use `patche_apply` with `reverse: true` to undo a patch

This workflow allows you to maintain a collection of modifications that can be applied to multiple projects or versions of code.

Would you like specific help with any of these steps?
"""

patche_examples_prompt = """
<user>

Can you show me some examples of using Patche commands?

</user>

# Patche Command Examples

Here are some practical examples of using Patche commands:

**Listing patches in a directory:**
```json
{
  "patche_dir": "/path/to/patches"
}
```

**Viewing a specific patch's details:**
```json
{
  "patch_path": "/path/to/patches/feature-fix.patch"
}
```

**Applying a patch:**
```json
{
  "patch_path": "/path/to/patches/feature-fix.patch",
  "target_dir": "/path/to/project"
}
```

**Reversing a previously applied patch:**
```json
{
  "patch_path": "/path/to/patches/feature-fix.patch",
  "target_dir": "/path/to/project",
  "reverse": true
}
```

Would you like me to help you execute any of these commands?
"""

# List of all prompts
prompts: list[Prompt] = [
    Prompt(
        name="base_info",
        description="Basic information about the Patche tool",
        description_zh="Basic info of the Patche toolchain",
        content=base_info_prompt,
    ),
    Prompt(
        name="show_config",
        description="Show the configuration of Patche",
        content=show_config_prompt,
        arguments=[
            {"name": "config_path", "type": "string", "required": False},
            {"name": "patche_dir", "type": "string", "required": True},
        ],
    ),
    Prompt(
        name="list_patches",
        description="List all patches in a directory",
        content=list_prompt,
        arguments=[{"name": "patche_dir", "type": "string", "required": True}],
    ),
    Prompt(
        name="show_patch",
        description="Show detailed information about a patch",
        content=show_prompt,
        arguments=[{"name": "patch_path", "type": "string", "required": True}],
    ),
    Prompt(
        name="apply_patch",
        description="Apply a patch to a target directory",
        content=apply_prompt,
        arguments=[
            {"name": "patch_path", "type": "string", "required": True},
            {"name": "target_dir", "type": "string", "required": True},
            {"name": "reverse", "type": "boolean", "required": False},
        ],
    ),
    Prompt(
        name="reverse_apply",
        description="Reverse apply a patch to a target directory",
        content=reverse_apply_prompt,
        arguments=[
            {"name": "patch_path", "type": "string", "required": True},
            {"name": "target_dir", "type": "string", "required": True},
        ],
    ),
    Prompt(
        name="help",
        description="Show help information about Patche commands",
        content=help_prompt,
    ),
    Prompt(
        name="patch_creation",
        description="Guide for creating new patches",
        content=patch_creation_guidance_prompt,
    ),
    Prompt(
        name="workflow",
        description="Explain the typical Patche workflow",
        content=patche_workflow_prompt,
    ),
    Prompt(
        name="examples",
        description="Show examples of using Patche commands",
        content=patche_examples_prompt,
    ),
]
