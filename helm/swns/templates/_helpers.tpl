{{/*
Expand the name of the chart.
*/}}
{{- define "swns.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}


{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "swns.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}


{{/*
Create Database app name
*/}}
{{- define "swns.db.fullname" -}}
{{- $name := default .Chart.Name }}
{{- if contains $name .Release.Name }}
{{- printf "%s-%s" "db" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s-%s" "db" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end}}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "swns.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}


{{/*
Django Common labels
*/}}
{{- define "swns.labels" -}}
helm.sh/chart: {{ include "swns.chart" . }}
{{ include "swns.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}


{{/*
Django Selector labels
*/}}
{{- define "swns.selectorLabels" -}}
app.kubernetes.io/name: {{ include "swns.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}


{{/*
PostgreSQL Common labels
*/}}
{{- define "swns.db.labels" -}}
helm.sh/chart: {{ include "swns.chart" . }}
{{ include "swns.db.selectorLabels" . }}
release: {{ .Release.Name }}
app.kubernetes.io/managed-by: helm
{{- end }}


{{/*
PostgreSQL Selector labels
*/}}
{{- define "swns.db.selectorLabels" -}}
app: db-{{ .Release.Name }}
{{- end }}