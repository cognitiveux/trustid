//
//  InstructorExaminationAction.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/11/21.
//

import Foundation

enum InstructorExaminationAction:String, CaseIterable, ExaminationAction{
    case start = "Start Exam"
    case information = "Information"
    case privacyPolicy = "Privacy Policy"
    case enrolledStudents = "Enrolled Students"
    //case report = "Report"
    //case edit = "Edit Exam"
    
    var id: RawValue { rawValue }
}
