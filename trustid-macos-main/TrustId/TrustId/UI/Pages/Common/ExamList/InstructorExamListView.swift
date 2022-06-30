//
//  InstructorExamListView.swift
//  TrustId
//
//  Created by Adamos Adamou on 11/1/22.
//

import SwiftUI

extension InstructorExam: Identifiable { }

struct InstructorExamListView: View {
    
    public let exams:[InstructorExam]
  
    @Binding public var selectedExam:InstructorExam
    
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
    
    func map(_ exam:InstructorExam) -> Exam{
        .init(id: exam.id, name: exam.name, status: exam.status, scheduled: exam.scheduled)
    }
    
    func map(_ exams:[InstructorExam]) -> [Exam]{
        exams.map{map($0)}
    }
}
