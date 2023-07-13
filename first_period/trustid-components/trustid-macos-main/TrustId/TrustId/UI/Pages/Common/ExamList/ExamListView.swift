//
//  ExamListView.swift
//  TrustId
//
//  Created by Adamos Adamou on 27/11/21.
//

import SwiftUI

extension Exam: Identifiable { }

struct ExamListView: View {
    
    public let exams:[Exam]
  
    @Binding public var selectedExam:Exam
    
    public var allowSelection = true
    
    var body: some View {
        ExamListViewBase(
            exams: exams,
            selectedExam: selectedExam,
            allowSelection: allowSelection
        ) { exam in
            selectedExam = exam
        }
    }
}
