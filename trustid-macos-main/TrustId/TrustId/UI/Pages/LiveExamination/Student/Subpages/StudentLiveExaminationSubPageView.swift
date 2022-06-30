//
//  StudentLiveExaminationSubPageView.swift
//  TrustId
//
//  Created by Adamos Adamou on 28/12/21.
//

import SwiftUI

struct StudentLiveExaminationSubPageView: View {
    
    public let viewModel:StudentLiveExaminationSubPageViewModel
    
    @EnvironmentObject var videoViewModel:VideoPreviewViewModel
    
    private static let refreshSeconds:Double = 25// 60 * 1
    
    private let timer = Timer
        .publish(every: refreshSeconds, on: .main, in: .common)
        .autoconnect()
    
    var body: some View {
        StudentLiveExaminationLayout {
            VStack(alignment:.leading){
                Text("Examination Questions")
                    .font(.custom("Roboto", size: 17))
                    .bold()
                    .padding(16)
                Spacer()
                WebView(url: "https://trustid-project.eu/exam-q.html")
            }
            .frame(maxWidth:.infinity)
            
        } statusContent: {
            VStack{
                MonitoringView()
                Spacer()
                Divider()
                UserFeedbackView(
                    viewModel: .init(exam_id: viewModel.exam_id)
                )
                Spacer()
            }
        } actionContent: {
            HStack{
                Spacer()
                
                Button("Leave Exam") {
                    viewModel.leaveExam()
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(RedButton())
            }
            .padding()
        }
        .addNavigationHeader(showOnlyLogo: true)
        .onReceive(timer, perform: runIdentification)
    }
    
    private func runIdentification(date:Date){
        videoViewModel.toggleSession()
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            videoViewModel.capturePhoto { image in
                self.videoViewModel.toggleSession()
                self.viewModel.executeMonitoringRequest(capturedImage: image)
            }
        }
    }
}

struct StudentLiveExaminationSubPageView_Previews: PreviewProvider {
    static var previews: some View {
        StudentLiveExaminationSubPageView(
            viewModel: .init(exam_id: "test_exam_id")
        )
        .environmentObject(VideoPreviewViewModel())
    }
}
