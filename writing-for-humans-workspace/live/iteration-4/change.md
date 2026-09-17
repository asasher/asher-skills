# Automatic discovery baseline

Human feedback: naming writing-for-humans and unslop in the prompt defeats testing normal use. writing-for-humans depends on unslop; both should be available without the user naming either.

Start a new baseline with the original version 1 packages from commit 40b183c, matching iteration 2's SKILL.md hashes. Copy the complete packages, including allow_implicit_invocation settings, into the clean temporary repo. The prompt is exactly the topic. No extra AGENTS.md or activation directive is added.

Version 2 remains the working-tree candidate, unchanged. Trial it later under this same setup. Earlier explicit-invocation transcripts remain evidence of that different setup.

Discovery and observable skill reads are separate from the human's assessment of the replies. A skill being available does not establish that the model used it. Observe logs without prompting the participant about this distinction.
