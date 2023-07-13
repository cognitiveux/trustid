//
//  StudentExaminationAction.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/11/21.
//

import Foundation

enum StudentExaminationAction:String, CaseIterable, ExaminationAction{
    case join = "Join Exam"
    case information = "Information"
    case privacyPolicy = "Privacy Policy"
    // case report = "Report"
    
    var id: RawValue { rawValue }
}
