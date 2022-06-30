//
//  IdentificationContentView.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import SwiftUI

struct IdentificationContentView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    @EnvironmentObject var videoViewModel:VideoPreviewViewModel
    
    @State var currentPhoto:NSImage?
    
    public var identifitationCompleted: ()->Void
    
    var body: some View{
        makeCurrentStepView()
            .onAppear {
                viewModel.capturedPhoto = capturedPhotoCallback
            }
            .sheet(isPresented: $viewModel.showIdentityConfirmationDialog){
                IdentityConfirmationView(){
                    currentPhoto = nil
                }
                .environmentObject(viewModel)
            }
            .sheet(isPresented: $viewModel.showIdentificationFailureDialog){
                IdentificationFailureView(){
                    currentPhoto = nil
                }
                .environmentObject(viewModel)
            }
            .sheet(isPresented: $viewModel.showInstructorIdentityConfirmationDialog){
                InstructorIdentityConfirmationView()
                    .environmentObject(viewModel)
            }
    }
    
    private func capturedPhotoCallback()->NSImage?{
        return currentPhoto
    }
    
    @ViewBuilder
    func makeCurrentStepView() -> some View{
        switch viewModel.currentStep{
        
        case .getStarted:
            GetStartedStepView()
       
        case .face, .confirmIdentity:
            if let photo = currentPhoto {
                SplitViewLayout{
                    Image(nsImage: photo)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                } bottomContent: { EmptyView() }
            } else {
                FaceIdentificationStepView(){ image in
                    currentPhoto = image
                    videoViewModel.toggleSession()
                }
            }
            
        case .runningApplications:
            RunningApplicationStepView()
            
        case .identified:
            IdentifiedStepView {
                identifitationCompleted()
            }
            
        }
    }
}

struct IdentificationContentView_Previews: PreviewProvider {
    static var previews: some View {
        IdentificationContentView{
            // do nothing
        }
        .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
        .environmentObject(VideoPreviewViewModel())
    }
}
