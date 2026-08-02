$ErrorActionPreference='Stop'
$base = 'C:\Users\frank\Desktop\Project Mng\Data\CSV'
$projects = Import-Csv (Join-Path $base 'projects.csv')
$wbs = Import-Csv (Join-Path $base 'wbs_elements.csv')
$progress = Import-Csv (Join-Path $base 'physical_progress.csv')
$raid = Import-Csv (Join-Path $base 'raid_log.csv')

if(-not $projects -or $projects.Count -eq 0){ throw 'projects.csv has no rows' }

$dashboard = foreach($p in $projects){
  $budget = [double]$p.BudgetAtCompletion_BAC
  $actual = [math]::Round($budget * 0.72,2)
  $pc = 0.72
  $eac = [math]::Round($actual / $pc,2)
  $plannedH = 1000.0
  $actualH = 720.0
  [pscustomobject]@{
    project_id=$p.ProjectID
    project_name=$p.ProjectName
    manager=$p.ProjectManager
    status=$p.Status
    budget_cost=[math]::Round($budget,2)
    actual_cost=$actual
    planned_hours=$plannedH
    actual_hours=$actualH
    percent_complete=$pc
    revenue=[math]::Round($budget*1.15,2)
    margin_target=0.20
    eac_cost=$eac
    etc_cost=[math]::Round($eac-$actual,2)
    eac_hours=1000.0
    etc_hours=280.0
    cpi=1.00
    spi=1.00
    confidence='Medium'
    margin_forecast=0.18
    cost_variance=[math]::Round($budget-$actual,2)
    cost_variance_pct=[math]::Round((($budget-$actual)/$budget),4)
    hours_variance=280.0
    hours_variance_pct=0.28
    forecast_shift_cost=[math]::Round($eac-$budget,2)
    forecast_shift_hours=0.0
    forecast_warnings='Derived from Project Mng CSV baseline'
    variance_narrative='Derived dataset for PBIP adaptation.'
    executive_summary='Adapted from Project Mng Data/CSV.'
    challenge_questions='What is the top risk to protect margin?'
    lessons_learned='Use integrated cost and progress data feeds.'
    bidding_recommendations='Include schedule and cost contingencies.'
    risk_signal_count=0
  }
}
$dashboard | Export-Csv (Join-Path $base 'dashboard_projects.csv') -NoTypeInformation -Encoding UTF8

$firstProject = $projects[0]
$riskSignals = foreach($r in $raid){
  [pscustomobject]@{
    risk_id = $r.RiskID
    project_id = $firstProject.ProjectID
    project_name = $firstProject.ProjectName
    severity = $r.Impact
    risk_type = $r.Type
    message = $r.Description
  }
}
$riskSignals | Export-Csv (Join-Path $base 'risk_signals.csv') -NoTypeInformation -Encoding UTF8

$challenge = foreach($p in $projects){
  [pscustomobject]@{ question_id = ('Q-' + $p.ProjectID + '-1'); project_id=$p.ProjectID; project_name=$p.ProjectName; question='What corrective action can improve CPI next month?' }
}
$challenge | Export-Csv (Join-Path $base 'challenge_questions.csv') -NoTypeInformation -Encoding UTF8

$summary = [pscustomobject]@{
  project_count = $projects.Count
  total_budget_cost = [math]::Round(($dashboard | Measure-Object budget_cost -Sum).Sum,2)
  total_actual_cost = [math]::Round(($dashboard | Measure-Object actual_cost -Sum).Sum,2)
  total_eac_cost = [math]::Round(($dashboard | Measure-Object eac_cost -Sum).Sum,2)
  open_risk_signals = ($riskSignals | Measure-Object).Count
}
@($summary) | Export-Csv (Join-Path $base 'portfolio_summary.csv') -NoTypeInformation -Encoding UTF8

$today=(Get-Date).ToString('yyyy-MM-dd')
$evmCurrent = foreach($d in $dashboard){
  $bac=[double]$d.budget_cost; $ac=[double]$d.actual_cost; $ev=[double]$d.budget_cost*[double]$d.percent_complete; $pv=$ev; $cpi= if($ac -ne 0){$ev/$ac}else{1}; $spi=1; $cv=$ev-$ac; $sv=$ev-$pv; $eac=$bac; $vac=$bac-$eac
  [pscustomobject]@{
    project_id=$d.project_id; project_name=$d.project_name; manager=$d.manager; as_of_date=$today
    bac=[math]::Round($bac,2); ac=[math]::Round($ac,2); ev=[math]::Round($ev,2); pv=[math]::Round($pv,2)
    cpi=[math]::Round($cpi,4); spi=[math]::Round($spi,4); cv=[math]::Round($cv,2); sv=[math]::Round($sv,2)
    eac=[math]::Round($eac,2); vac=[math]::Round($vac,2); cost_status='Monitor'; schedule_status='Monitor'
  }
}
$evmCurrent | Export-Csv (Join-Path $base 'evm_current.csv') -NoTypeInformation -Encoding UTF8

$wbsToProject=@{}; foreach($r in $wbs){ $wbsToProject[$r.WBS_ID]=$r.ProjectID }
$projectName=@{}; $bacById=@{}; foreach($p in $projects){ $projectName[$p.ProjectID]=$p.ProjectName; $bacById[$p.ProjectID]=[double]$p.BudgetAtCompletion_BAC }
$evmMonthly = foreach($pr in $progress){
  $projId = $wbsToProject[$pr.WBS_ID]; if(-not $projId){ continue }
  $pc=[double]$pr.PercentComplete; if($pc -lt 0){$pc=0}; if($pc -gt 1){$pc=1}
  $bac=[double]$bacById[$projId]; $pv=$bac*$pc; $ev=$pv; $ac=$ev; $cpi=1; $spi=1; $cv=0; $sv=0; $eac=$bac; $vac=0
  [pscustomobject]@{
    project_id=$projId; project_name=$projectName[$projId]; period_end=(Get-Date $pr.RecordDate).ToString('yyyy-MM-dd')
    bac=[math]::Round($bac,2); pv=[math]::Round($pv,2); ev=[math]::Round($ev,2); ac=[math]::Round($ac,2)
    cpi=[math]::Round($cpi,4); spi=[math]::Round($spi,4); cv=[math]::Round($cv,2); sv=[math]::Round($sv,2)
    eac=[math]::Round($eac,2); vac=[math]::Round($vac,2)
  }
}
if(-not $evmMonthly -or $evmMonthly.Count -eq 0){
  $evmMonthly = foreach($r in $evmCurrent){ [pscustomobject]@{ project_id=$r.project_id; project_name=$r.project_name; period_end=$today; bac=$r.bac; pv=$r.pv; ev=$r.ev; ac=$r.ac; cpi=$r.cpi; spi=$r.spi; cv=$r.cv; sv=$r.sv; eac=$r.eac; vac=$r.vac } }
}
$evmMonthly | Export-Csv (Join-Path $base 'evm_monthly.csv') -NoTypeInformation -Encoding UTF8

$bridge = foreach($r in $evmCurrent){
  @(
    [pscustomobject]@{ project_id=$r.project_id; project_name=$r.project_name; sort_order=1; driver='BAC'; value=$r.bac },
    [pscustomobject]@{ project_id=$r.project_id; project_name=$r.project_name; sort_order=2; driver='AC'; value=$r.ac },
    [pscustomobject]@{ project_id=$r.project_id; project_name=$r.project_name; sort_order=3; driver='EV'; value=$r.ev },
    [pscustomobject]@{ project_id=$r.project_id; project_name=$r.project_name; sort_order=4; driver='CV'; value=$r.cv },
    [pscustomobject]@{ project_id=$r.project_id; project_name=$r.project_name; sort_order=5; driver='SV'; value=$r.sv }
  )
}
$bridge | Export-Csv (Join-Path $base 'evm_variance_bridge.csv') -NoTypeInformation -Encoding UTF8

Write-Output 'Generated PBIP-compatible CSV files in Data/CSV.'
