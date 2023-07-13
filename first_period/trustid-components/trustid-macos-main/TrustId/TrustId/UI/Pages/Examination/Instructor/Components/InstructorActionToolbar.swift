//
//  InstructorActionToolbar.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/11/21.
//

import SwiftUI

struct InstructorActionToolbar: View {
    public var actions: [InstructorExaminationAction]
    public var selectedAction:Binding<InstructorExaminationAction?>
    public var didSelect: (InstructorExaminationAction)->Void
   
    var body: some View {
        HStack{
            Button(InstructorExaminationAction.start.rawValue){
                didSelect(.start)
            }
            .font(.custom("Roboto", size: 13))
            .buttonStyle(BlueButton())
            Spacer()
            ForEach(subpageActions){ action in
                Button(action.rawValue){
                    didSelect(action)
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(WhiteButton(isSelected: isSelected(action)))
            }
            Spacer()
        }
    }
    
    private var subpageActions: [InstructorExaminationAction]{
        guard actions.count > 0 else { return [] }
        return actions.filter{ $0 != .start }
    }
    
    private func isSelected(_ action:InstructorExaminationAction) -> Bool{
        return action.rawValue == selectedAction.wrappedValue?.rawValue ?? "-"
    }
}

struct InstructorActionToolbar_Previews: PreviewProvider {
    
    static var actions = InstructorExaminationAction.allCases
    static var selectedAction:Binding<InstructorExaminationAction?> = .constant(.information)
    
    static var previews: some View {
        InstructorActionToolbar(actions: actions, selectedAction: selectedAction){ action in
            print("action \(action.rawValue)")
        }
    }
}
