//
//  ExamListViewBase.swift
//  TrustId
//
//  Created by Adamos Adamou on 11/1/22.
//

import SwiftUI

struct ExamListViewBase: View {

    public let exams:[Exam]
    public let selectedExam:Exam
    public let allowSelection:Bool
    public var selectionHandler: (Exam) -> Void
    
    var body: some View {
        List(exams){ exam in
            VStack{
                HStack(spacing:0){
                    VStack{
                        Circle()
                            .foregroundColor(
                                exam.isStarted
                                ? TrustIdPalette.green
                                : .gray
                            )
                            .frame(width: 10, height: 10)
                            .clipped()
                            .offset(.zero)
                        Spacer()
                    }

                    VStack(spacing:0){
                        ExamDetailsView(exam: .init(exam: exam))
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                }
            }
            .padding(8)
            .background(isSelected(exam) ? TrustIdPalette.buttonBlue : Color.clear)
            .foregroundColor(isSelected(exam) ? Color.white : Color.black)
            .clipShape(RoundedRectangle(cornerRadius: 8))
            .onTapGesture { didSelect(exam) }
            
            if isLastExam(exam: exam) == false{
                Divider()
            }
        }
    }
    
    private func didSelect(_ exam:Exam){
        guard allowSelection else { return }
        selectionHandler(exam)
    }
    
    private func isSelected(_ exam:Exam) -> Bool{
        return exam.id == selectedExam.id
    }
    
    private func isLastExam(exam:Exam) -> Bool{
        guard let index = exams.firstIndex(where: {$0.id == exam.id}) else {
            return true
        }
        let itemDecimalPosition = index + 1
        return exams.count == itemDecimalPosition
    }
}

struct ExamListViewBase_Previews: PreviewProvider {
    
    static var exams:[Exam] = MockExamService.exams
    
    static var selectedExam:Exam = .empty
    
    static var previews: some View {
        ExamListViewBase(
            exams: exams,
            selectedExam: selectedExam,
            allowSelection: true
        ){ _ in }
        .frame(width: 400, height: 500)
    }
}
