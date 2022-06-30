//
//  StudentExaminationView.swift
//  TrustId
//
//  Created by Adamos Adamou on 27/11/21.
//

import SwiftUI

struct StudentExaminationView: View {
    
    @StateObject var viewModel = StudentExaminationViewModel()
    
    @State var selectedAction:StudentExaminationAction? = .information
    
    var body: some View {
        ExaminationLayout {
            StudentExamListView(exams: viewModel.exams, selectedExam: $viewModel.selectedExam)
        } examContent: {
            ExamDetailsView(exam: .init(exam: viewModel.selectedExam))
        } subPageContent: {
            VStack{
                StudentActionToolbar(
                    actions: StudentExaminationAction.allCases,
                    selectedAction: $selectedAction
                ){ action in
                    
                    if action == .join{
                        viewModel.joinExam()
                        return
                    }
                    
                    selectedAction = action
                }
                Spacer()
                renderSubPage(selectedAction: selectedAction)
            }
            .padding(.horizontal, 32)
        }
        .onAppear(perform: viewModel.loadExams)
        .addNavigationHeader()
        .overlay(LoadingView(isLoading: viewModel.isLoading))
    }
    
    @ViewBuilder
    private func renderSubPage(selectedAction:StudentExaminationAction?) -> some View{
     
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
        
        case .join, .none:
            EmptyView()
        }
    }
}

struct StudentExaminationView_Previews: PreviewProvider {
    static var previews: some View {
        StudentExaminationView()
    }
}
