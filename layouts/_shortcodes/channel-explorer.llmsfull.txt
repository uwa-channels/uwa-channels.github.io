{{- /* Plain-text outputs (page .md, llms-full.txt) get a link instead of the interactive iframe. */ -}}
{{- $site := .Get "site" | default "" -}}
{{- if $site -}}
Interactive diorama of this experiment (schematic): {{ printf "explorer/channel-%s.html" $site | absURL }}
{{- else -}}
Interactive map and dioramas of the experiments (schematic): {{ "explorer/channel-library.html" | absURL }}
{{- end -}}
