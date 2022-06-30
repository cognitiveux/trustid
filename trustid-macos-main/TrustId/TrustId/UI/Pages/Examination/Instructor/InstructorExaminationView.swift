//
//  InstructorExaminationView.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/11/21.
//

import SwiftUI

struct InstructorExaminationView: View {
    
    @StateObject var viewModel = InstructorExaminationViewModel()
    
    @State var selectedAction:InstructorExaminationAction? = .information
    
    var body: some View {
        ZStack{
            ExaminationLayout {
                InstructorExamListView(exams: viewModel.exams, selectedExam: $viewModel.selectedExam)
            } examContent: {
                ExamDetailsView(exam: .init(exam: viewModel.selectedExam))
            } subPageContent: {
                VStack{
                    InstructorActionToolbar(
                        actions: InstructorExaminationAction.allCases,
                        selectedAction: $selectedAction
                    ) { action in
                        
                        if action == .start{
                            viewModel.startExam()
                            return
                        }
                        
                        selectedAction = action
                    }
                    Spacer()
                    renderSubPage(selectedAction: selectedAction)
                }
                .padding(.horizontal, 32)
            }
        }
        .onAppear(perform: viewModel.loadExams)
        .addNavigationHeader()
        .overlay(LoadingView(isLoading: viewModel.isLoading))
    }
    
    @ViewBuilder
    private func renderSubPage(selectedAction:InstructorExaminationAction?) -> some View{
     
        switch selectedAction {

        case .information:
            ExaminationInformationView(
                additionalMaterial: viewModel.selectedExam.additionalMaterial,
                duration: viewModel.selectedExam.duration,
                examType: viewModel.selectedExam.examType
            )
            
        case .privacyPolicy:
            WebView(url: "https://trustid-project.eu/privacy_webview.php")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            
//        case .report:
//            Text("Report Content")
//                .font(.custom("Roboto", size: 13))
//                .frame(maxWidth: .infinity, maxHeight: .infinity)
            
        case .enrolledStudents:
            List(viewModel.selectedExam.enrolledStudents, id: \.email){ student in
                Text(student.email)
                    .font(.custom("Roboto", size: 13))
            }
            
//        case .edit:
//            Text("Edit Exam")
//                .font(.custom("Roboto", size: 13))
//                .frame(maxWidth: .infinity, maxHeight: .infinity)
            
        case .start, .none:
            EmptyView()
        }
    }
}

struct InstructorExaminationView_Previews: PreviewProvider {
    static var previews: some View {
        InstructorExaminationView()
    }
}
