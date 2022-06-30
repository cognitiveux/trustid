//
//  RunningApplicationStepView.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/12/21.
//

import SwiftUI

struct RunningApplicationStepView: View {
    
    @EnvironmentObject var viewModel:StudentIdentificationSubPageViewModel
    
    var body: some View {
        SplitViewLayout{
            VStack(spacing:32){
                
                Text("Checkup Report")
                    .font(.custom("Roboto", size: 20))
                    .bold()
                    .frame(height:60)
                
                if viewModel.runningApplicationsNeedsCheck{
                    Text("Pending")
                        .font(.custom("Roboto", size: 17))
                } else {
                    if viewModel.blockingApplications.count == 0{
                        Text("All good, please proceed")
                            .font(.custom("Roboto", size: 17))
                            .foregroundColor(TrustIdPalette.green)
                    } else {
                        blockingApplicationsView
                    }
                }
                
                Spacer()
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        } bottomContent: {
            VStack(spacing:0){
                Color.clear.frame(height:8)
                Divider()
                StepInfoView(
                    title: "TRUSTID will check your computer for any forbidden running applications and processes",
                    subTitle: nil
                ) {
                    HStack{
                        Button("Run Checkup"){
                            viewModel.executeStep()
                        }
                        .font(.custom("Roboto", size: 13))
                        .buttonStyle(BlueButton())
                        
                        Button("Proceed"){
                            viewModel.currentStep = .identified
                        }
                        .font(.custom("Roboto", size: 13))
                        .buttonStyle(BlueButton())
                        .disabled(isProceedButtonDisabled)
                    }
                }
            }
        }
    }
    
    private var isProceedButtonDisabled:Bool {
        return viewModel.runningApplicationsNeedsCheck
            || viewModel.blockingApplications.count > 0
    }
    
    private var blockingApplicationsView: some View{
        GeometryReader{ proxy in
            VStack{
                List(viewModel.blockingApplications, id: \.self){ application in
                    HStack(spacing:16){
                        HStack(spacing:8){
//                            Circle()
//                                .foregroundColor(TrustIdPalette.green)
//                                .frame(width:15, height: 15)
                            
                            Circle()
                                .foregroundColor(TrustIdPalette.red)
                                .frame(width:15, height: 15)
                        }
                        Text(application)
                            .font(.custom("Roboto", size: 15))
                    }.frame(height:50)
                }.frame(width: proxy.size.width * 0.7)
            }.frame(maxWidth:.infinity, maxHeight: .infinity)
        }
    }
}

struct RunningApplicationStepView_Previews: PreviewProvider {
    static var previews: some View {
        RunningApplicationStepView()
            .environmentObject(StudentIdentificationSubPageViewModel(exam_id: "-"))
    }
}
