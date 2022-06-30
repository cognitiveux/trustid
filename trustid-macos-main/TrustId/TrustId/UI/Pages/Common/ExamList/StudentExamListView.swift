//
//  StudentExamListView.swift
//  TrustId
//
//  Created by Adamos Adamou on 11/1/22.
//

import SwiftUI

extension StudentExam: Identifiable { }

struct StudentExamListView: View {
    
    public let exams:[StudentExam]
  
    @Binding public var selectedExam:StudentExam
    
    public var allowSelection = true
    
    var body: some View {
        
        ExamListViewBase(
            exams: map(exams),
            selectedExam: map(selectedExam),
            allowSelection: allowSelection
        ) { exam in
            if let exam = exams.first(where: {$0.id == exam.id}){
                selectedExam = exam
            }
        }
    }
    
    func map(_ exam:StudentExam) -> Exam{
        .init(id: exam.id, name: exam.name, status: exam.status, scheduled: exam.scheduled)
    }
    
    func map(_ exams:[StudentExam]) -> [Exam]{
        exams.map{map($0)}
    }
}
