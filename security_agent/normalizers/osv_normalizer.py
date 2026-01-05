from core.models import UnifiedFinding, DependencyFinding

class OSVNormalizer:
    
    @staticmethod
    def normalize(finding: list[DependencyFinding])-> list[UnifiedFinding]:
        
        normalized = []
        
        # usually every finding is high, unless there is a CVSS backed
        # then it becomes critical
        
        for f in finding:
            severity = "High"
            if f.severity and "CVSS" in f.severity:
                severity = "critical"
                
            unified = UnifiedFinding(
                source= "osv-scanner", 
                category= "dependency",
                severity=severity,
                confidence=f.confidence,
                identifier=f.vulnerability_id,
                message=f.summary or "Vulnerable dependency detected",
                package_name=f.package_name,
                installed_version=f.installed_version,
                fixed_version=f.fixed_version,
                references=f.references,
            )
        
            normalized.append(unified)
        
        return normalized