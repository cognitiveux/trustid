//
//  ExamDetailsView.swift
//  TrustId
//
//  Created by Adamos Adamou on 25/11/21.
//

import SwiftUI

public struct ExamDetail{

    public let id: String
    public let name: String
    public let status: String
    public let scheduledOn: String
    
    init(id: String, name: String, status: String, scheduled: Date) {
        self.id = id
        self.name = name
        self.status = status
        self.scheduledOn = ExamDetail.formattedScheduled(date: scheduled)
    }
    
    init(exam:Exam){
        self.id = exam.id
        self.name = exam.name
        self.status = exam.status
        self.scheduledOn = ExamDetail.formattedScheduled(date: exam.scheduled)
    }
    
    init(exam:StudentExam){
        self.id = exam.id
        self.name = exam.name
        self.status = exam.status
        self.scheduledOn = ExamDetail.formattedScheduled(date: exam.scheduled)
    }
    
    init(exam:InstructorExam){
        self.id = exam.id
        self.name = exam.name
        self.status = exam.status
        self.scheduledOn = ExamDetail.formattedScheduled(date: exam.scheduled)
    }
    
    private static func formattedScheduled(date: Date) -> String{
        let formatter = DateFormatter()
        formatter.dateFormat = "dd/MM/yyyy HH:mm"
        return formatter.string(from: date)
    }
}

struct ExamDetailsView: View {
    
    public let exam: ExamDetail
    
    var body: some View {
        VStack(alignment:.leading, spacing:8){
            Text(exam.name)
                .font(.custom("Roboto-Bold", size: 18))
                .frame(maxWidth: .infinity, alignment: .leading)
            
            VStack(alignment:.leading, spacing:2){
                detailLine(name: "Examinination ID:", detail: exam.id)
                detailLine(name: "Status:", detail: exam.status)
                detailLine(name: "Scheduled:", detail: exam.scheduledOn)
            }
            .padding(.init(top: 0, leading: 16, bottom: 0, trailing: 16))
        }
    }
    
    private func detailLine(name:String, detail:String) -> some View{
        HStack{
            Text(name)
                .font(.custom("Roboto", size: 13))
            Text(detail)
                .font(.custom("Roboto", size: 13))
        }
    }
}

struct ExamDetailsView_Previews: PreviewProvider {
    
    static var exam: Exam = MockExamService.exams.first!
    
    static var previews: some View {
        ExamDetailsView(exam: .init(exam: exam))
            .frame(width: 500, height: 500)
    }
}
