//
//  StudentIdentificationSubPageView.swift
//  TrustId
//
//  Created by Adamos Adamou on 28/12/21.
//

import SwiftUI

struct StudentIdentificationSubPageView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    @EnvironmentObject var videoViewModel:VideoPreviewViewModel
    
    public var identifitationCompleted: ()->Void
    
    var body: some View{
        LeftRightLayout.init(leftWidthPercentage: 0.75) {
            identificationContentView
        } rightContent: {
            HStack(spacing:0){
                Color.clear.frame(width:8)
                Divider()
                statusContentView
                    .padding(16)
            }
        }
        .addNavigationHeader(showOnlyLogo: true)
        .overlay(LoadingView(isLoading: viewModel.isLoading))
        .background(Color.white)
    }
    
    private var identificationContentView: some View{
        IdentificationContentView{
            self.identifitationCompleted()
        }
    }
    
    private var statusContentView: some View{
        VStack{
            IdentificationStatusView()
            
            Spacer()
          
            VStack{
                Button("Cancel and leave Exam") {
                    viewModel.leaveExam()
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(RedButton())
            }
            .padding()
            .frame(maxWidth: .infinity, alignment: .trailing)
        }
    }
}

struct StudentIdentificationSubPageView_Previews: PreviewProvider {
    static var previews: some View {
        StudentIdentificationSubPageView() {
            
        }
        .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
        .environmentObject(VideoPreviewViewModel())
    }
}
