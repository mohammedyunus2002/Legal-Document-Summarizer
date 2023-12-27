# templates/_helpers.tpl
{{- define "legal-document-summarizer.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name }}
{{- end -}}
