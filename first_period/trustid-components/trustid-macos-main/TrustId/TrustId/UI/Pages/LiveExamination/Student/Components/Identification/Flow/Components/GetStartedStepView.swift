//
//  GetStartedView.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/12/21.
//

import SwiftUI

struct GetStartedStepView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    @EnvironmentObject var videoViewModel:VideoPreviewViewModel
    
    @StateObject private var cameraStatusStore = CameraStatusStore()
    @State private var showPermissionDialog = false
    
    var body: some View {
        SplitViewLayout{
            VStack{
                Image("face")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
            .background(Color.black)
        } bottomContent:{
            VStack(spacing:0){
                Color.clear.frame(height:8)
                Divider()
                StepInfoView(
                    title: "TRUSTID will identify you based on your face characteristics",
                    subTitle: "First, position your face in the camera"
                ){
                    Button.init("Get Started") {
                        viewModel.executeStep()
                    }
                    .font(.custom("Roboto", size: 13))
                    .buttonStyle(BlueButton())
                    .disabled(isGetStartedDisabled)
                }
            }
        }
        .onAppear{
            cameraStatusStore.checkAuthorizationStatus()
            showPermissionDialog = cameraStatusStore.needsAuthorization
        }
        .sheet(isPresented: $showPermissionDialog) {
            CameraPermissionView(isPresented: $showPermissionDialog)
        }
    }
    
    private var isGetStartedDisabled:Bool{
        !cameraStatusStore.hasCamera() || cameraStatusStore.needsAuthorization
    }
}

struct GetStartedView_Previews: PreviewProvider {
    static var previews: some View {
        GetStartedStepView()
            .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
    }
}
