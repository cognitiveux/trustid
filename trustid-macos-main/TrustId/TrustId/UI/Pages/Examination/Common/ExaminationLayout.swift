//
//  ExaminationLayout.swift
//  TrustId
//
//  Created by Adamos Adamou on 27/11/21.
//

import SwiftUI

struct ExaminationLayout<ListContent:View, ExamContent:View, SubPageContent:View>: View{
    
    public let listContent: () -> ListContent
    public let examContent: () -> ExamContent
    public let subPageContent: () -> SubPageContent
    
    var body: some View {
        GeometryReader{ proxy in
            HStack{
                listContent()
                Divider()
                VStack{
                    VStack{
                        examContent()
                    }
                    .frame(maxWidth: .infinity, alignment:.leading)
                    .padding(.horizontal, 32)
                    .padding(.top, 16)
                    .padding(.bottom, 32)
                    Spacer()
                    subPageContent()
                    Spacer()
                }
                .frame(width:proxy.size.width*0.725)
            }
        }
    }
}

struct ExaminationLayout_Previews: PreviewProvider {
    
    static var exams = ExamListViewBase_Previews.exams
    static var selectedExam = exams.first ?? .empty
    
    static var previews: some View {
        ExaminationLayout {
            ExamListView(exams: exams, selectedExam: .constant(selectedExam))
        } examContent: {
            ExamDetailsView(exam: .init(exam: selectedExam))
        } subPageContent: {
            Text("page content")
                .font(.custom("Roboto", size: 13))
        }
    }
}
