//
//  FaceIdentificationStepView.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/12/21.
//

import SwiftUI

struct FaceIdentificationStepView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    @EnvironmentObject var videoViewModel:VideoPreviewViewModel
    
    public let capturedPhoto: (NSImage)->Void
    
    var body: some View {
        SplitViewLayout{
            ZStack{
                VideoPreviewView(
                    session: videoViewModel.session,
                    startSessionCallback: {
                        videoViewModel.toggleSession()
                    }
                )
                
//                RoundedRectangle(cornerRadius: 16)
//                    .stroke(Color.gray, lineWidth: 2)
//                    .frame(width: 200, height: 200)
            }
            .padding()
            .background(Color.black)
        } bottomContent: {
            VStack(spacing:0){
                Color.clear.frame(height:8)
                Divider()
                StepInfoView(
                    title: "Position your face within the camera frame and look forward",
                    subTitle: nil
                ){
                    HStack{
                        switch viewModel.showRequestInstructorApprovalButton{
                        case .hidden:
                            Button.init("Capture") {
                                videoViewModel.capturePhoto { image in
                                    capturedPhoto(image)
                                    viewModel.executeStep()
                                }
                            }
                            .font(.custom("Roboto", size: 13))
                            .buttonStyle(BlueButton())
                            
                        case .visible:
                            Button.init("Request instructor's approval") {
                                viewModel.showRequestInstructorApprovalButton = .disabled
                                viewModel.requestIntructorApproval()
                            }
                            .font(.custom("Roboto", size: 13))
                            .buttonStyle(BlueButton())
                            .disabled(viewModel.showRequestInstructorApprovalButton == .disabled)
                            
                        case .disabled:
                            VStack{
                                ProgressView("Waiting for instructor's approval")
                                    .font(.custom("Roboto", size: 13))
                                Spacer()
                            }
                        }
                    }
                }
            }
        }
    }
}

struct FaceIdentificationStepView_Previews: PreviewProvider {
    static var previews: some View {
        FaceIdentificationStepView{ _ in }
        .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
        .environmentObject(VideoPreviewViewModel())
    }
}
