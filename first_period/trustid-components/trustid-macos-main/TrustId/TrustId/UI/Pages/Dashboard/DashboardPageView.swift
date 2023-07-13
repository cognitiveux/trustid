//
//  DashboardPageView.swift
//  TrustId
//
//  Created by Adamos Adamou on 22/11/21.
//

import SwiftUI

struct DashboardPageView: View {
    
    @StateObject public var viewModel = DashboardPageViewModel()
    
    private let buttonFactory = DashboardButtonConfigurationFactory()
    
    @State var maxHeight:CGFloat?
    
    @StateObject private var cameraStatusStore = CameraStatusStore()
    @State private var showPermissionDialog = false
    
    var body: some View {
        DashboardSplitLayout(leftContent: {
            leftToolbar
                .overlay(DetermineHeight())
        }, rightContent: {
            VStack(spacing:0){
                HStack{
                    Text("Upcoming Examinations")
                        .font(.custom("Roboto", size: 15))
                        .fontWeight(.semibold)
                    Spacer()
                }.padding()
            
                ExamListView(
                    exams: viewModel.exams,
                    selectedExam: .constant(viewModel.defaultExam),
                    allowSelection: false
                )
            }
            .overlay(listBorder)
            .frame(width: 350, height:maxHeight)
        })
        .onPreferenceChange(DetermineHeight.Key.self){
            maxHeight = $0 + 32 + 16
        }
        .padding()
        .background(Color.white)
        .onAppear(perform: viewModel.loadExams)
        .addNavigationHeader()
        .overlay(LoadingView(isLoading: viewModel.isLoading))
        .onAppear{
            cameraStatusStore.checkAuthorizationStatus()
            showPermissionDialog = cameraStatusStore.needsAuthorization
        }
        .sheet(isPresented: $showPermissionDialog) {
            CameraPermissionView(isPresented: $showPermissionDialog)
        }
        .sheet(isPresented: $viewModel.showErrorDialog){
            ErrorView(message: viewModel.showErrorDialogMessage)
        }
    }
    
    private var leftToolbar:some View{
        VStack(spacing:32){
            DashboardButton(configuration: buttonFactory.makeView())
                .onTapGesture(perform: viewModel.tappedViewExams)
            DashboardButton(configuration: buttonFactory.makeJoin())
                .onTapGesture(perform: viewModel.tappedJoinExam)
                .hidden()
        }
    }
    
    private var listBorder: some View {
        RoundedRectangle(cornerRadius: 8)
            .strokeBorder(Color.gray, lineWidth: 0.25)
    }
}

struct DashboardPageView_Previews: PreviewProvider {
    static var previews: some View {
        DashboardPageView()
    }
}
