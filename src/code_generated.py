from manim import *

class NeuralNetworkBackprop(Scene):
    def construct(self):
        # Neural Network setup
        input_layer = self.create_neuron_layer(3, LEFT * 4, "Input")
        hidden_layer = self.create_neuron_layer(4, ORIGIN, "Hidden")
        output_layer = self.create_neuron_layer(2, RIGHT * 4, "Output")
        
        # Connections
        input_to_hidden = self.create_connections(input_layer, hidden_layer)
        hidden_to_output = self.create_connections(hidden_layer, output_layer)
        
        # Group all layers and connections
        network = VGroup(
            input_layer, hidden_layer, output_layer,
            input_to_hidden, hidden_to_output
        )
        
        # Step 1: Display the network
        self.play(Create(network))
        self.wait()
        
        # Step 2: Forward Pass
        input_values = [0.8, 0.2, 0.5]
        hidden_values = [0.7, 0.6, 0.3, 0.8]
        output_values = [0.4, 0.7]
        
        self.forward_pass_animation(
            input_layer, hidden_layer, output_layer,
            input_to_hidden, hidden_to_output,
            input_values, hidden_values, output_values
        )
        
        # Step 3: Error Calculation
        target_values = [0.9, 0.1]
        error = self.error_calculation(output_layer, output_values, target_values)
        self.wait()
        
        # Step 4: Backpropagation
        self.backpropagation_animation(
            input_layer, hidden_layer, output_layer,
            input_to_hidden, hidden_to_output
        )
        
        # Step 5: Weight Updates
        self.weight_update_animation(input_to_hidden, hidden_to_output)
        
        # Step 6: Second Forward Pass with Improved Predictions
        improved_output_values = [0.6, 0.5]  # Closer to targets
        self.forward_pass_animation(
            input_layer, hidden_layer, output_layer,
            input_to_hidden, hidden_to_output,
            input_values, hidden_values, improved_output_values
        )
        
        improved_error = self.error_calculation(
            output_layer, improved_output_values, target_values, "Improved Error"
        )
        
        # Step 7: Iterate a few more times
        for i in range(2):
            # Quick backprop animation
            self.backpropagation_animation(
                input_layer, hidden_layer, output_layer,
                input_to_hidden, hidden_to_output,
                duration=0.5
            )
            
            # Quick weight update
            self.weight_update_animation(input_to_hidden, hidden_to_output, duration=0.5)
            
            # Quick forward pass with better values
            next_improved = [0.75, 0.3] if i == 0 else [0.85, 0.15]
            self.forward_pass_animation(
                input_layer, hidden_layer, output_layer,
                input_to_hidden, hidden_to_output,
                input_values, hidden_values, next_improved,
                duration=0.5
            )
            
            # Show reducing error
            label = "Further Improved" if i == 0 else "Final Error"
            next_error = self.error_calculation(
                output_layer, next_improved, target_values, label, duration=0.5
            )
            if i == 0:
                self.play(FadeOut(improved_error))
                improved_error = next_error
            else:
                self.play(FadeOut(improved_error))
        
        # Fade out previous elements
        self.play(
            FadeOut(network),
            FadeOut(next_error)
        )
        
        # Step 8: Learning curve
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1, 0.2],
            axis_config={"include_tip": False},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        )
        
        x_label = Text("Training Iterations", font_size=24).next_to(axes, DOWN)
        y_label = Text("Error", font_size=24).next_to(axes, LEFT).rotate(PI/2)
        
        # Create the learning curve
        curve_points = [
            (0, 0.9),
            (1, 0.7),
            (2, 0.55),
            (3, 0.4),
            (4, 0.3),
            (5, 0.22),
            (6, 0.18),
            (7, 0.15),
            (8, 0.13),
            (9, 0.12),
            (10, 0.11)
        ]
        
        learning_curve = VMobject()
        learning_curve.set_points_smoothly([axes.c2p(x, y) for x, y in curve_points])
        learning_curve.set_color(BLUE)
        learning_curve.set_stroke(width=4)
        
        # Show the learning curve
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(learning_curve), run_time=3)
        
        # Highlight the decreasing error
        error_dot = Dot(axes.c2p(0, 0.9), color=RED)
        self.play(FadeIn(error_dot))
        self.play(error_dot.animate.move_to(axes.c2p(10, 0.11)), run_time=3)
        
        # Final explanation text
        final_text = Text("Neural Network Learning Process", font_size=36).to_edge(UP)
        self.play(Write(final_text))
        self.wait(2)

    def create_neuron_layer(self, num_neurons, position, label_text):
        neurons = VGroup(*[Circle(radius=0.3, fill_opacity=0.3, color=BLUE) 
                         for _ in range(num_neurons)])
        neurons.arrange(DOWN, buff=0.5)
        neurons.move_to(position)
        
        label = Text(label_text, font_size=20).next_to(neurons, UP, buff=0.5)
        
        return VGroup(neurons, label)
    
    def create_connections(self, layer1, layer2):
        connections = VGroup()
        neurons1 = layer1[0]  # Get the neurons from the layer
        neurons2 = layer2[0]
        
        for n1 in neurons1:
            for n2 in neurons2:
                line = Line(n1.get_center(), n2.get_center(), 
                           stroke_width=1, color=GRAY)
                connections.add(line)
        
        return connections
    
    def forward_pass_animation(self, input_layer, hidden_layer, output_layer,
                             input_to_hidden, hidden_to_output,
                             input_values, hidden_values, output_values,
                             duration=2):
        # Animate input neurons activation
        input_animations = []
        for i, neuron in enumerate(input_layer[0]):
            value = input_values[i]
            input_animations.append(
                neuron.animate.set_fill(BLUE, opacity=value)
            )
        self.play(*input_animations, run_time=duration/3)
        
        # Animate connections to hidden layer
        self.play(
            input_to_hidden.animate.set_color(BLUE_B),
            run_time=duration/3
        )
        
        # Animate hidden neurons activation
        hidden_animations = []
        for i, neuron in enumerate(hidden_layer[0]):
            value = hidden_values[i]
            hidden_animations.append(
                neuron.animate.set_fill(BLUE, opacity=value)
            )
        self.play(*hidden_animations, run_time=duration/3)
        
        # Animate connections to output layer
        self.play(
            hidden_to_output.animate.set_color(BLUE_B),
            run_time=duration/3
        )
        
        # Animate output neurons activation
        output_animations = []
        for i, neuron in enumerate(output_layer[0]):
            value = output_values[i]
            output_animations.append(
                neuron.animate.set_fill(BLUE, opacity=value)
            )
        self.play(*output_animations, run_time=duration/3)
        
        # Add value labels to output neurons
        output_labels = []
        for i, neuron in enumerate(output_layer[0]):
            value = output_values[i]
            label = Text(f"{value:.1f}", font_size=16).next_to(neuron, RIGHT)
            output_labels.append(label)
        
        self.play(*[Write(label) for label in output_labels], run_time=duration/3)
        
        return VGroup(*output_labels)
    
    def error_calculation(self, output_layer, output_values, target_values, label="Error", duration=2):
        # Create target value display
        target_display = VGroup()
        for i, neuron in enumerate(output_layer[0]):
            value = output_values[i]
            target = target_values[i]
            error = abs(value - target)
            
            neuron_pos = neuron.get_center()
            
            # Create target circle
            target_circle = Circle(radius=0.3, fill_opacity=target, 
                                 fill_color=GREEN, stroke_color=GREEN)
            target_circle.move_to(neuron_pos + RIGHT * 1.5)
            
            # Create labels
            pred_label = Text(f"Pred: {value:.1f}", font_size=14).next_to(neuron, RIGHT, buff=0.2)
            target_label = Text(f"Target: {target:.1f}", font_size=14).next_to(target_circle, RIGHT, buff=0.2)
            error_value = Text(f"Error: {error:.1f}", font_size=14, color=RED).next_to(
                target_label, RIGHT, buff=0.5)
            
            target_display.add(target_circle, pred_label, target_label, error_value)
        
        error_title = Text(label, font_size=20, color=RED).to_edge(UP)
        target_display.add(error_title)
        
        self.play(Write(target_display), run_time=duration)
        
        return target_display
    
    def backpropagation_animation(self, input_layer, hidden_layer, output_layer,
                                input_to_hidden, hidden_to_output, duration=2):
        # Create backward gradient arrows
        gradient_arrows = VGroup()
        
        # Arrows from output to hidden layer
        for o_neuron in output_layer[0]:
            for h_neuron in hidden_layer[0]:
                arrow = Arrow(
                    o_neuron.get_center(), h_neuron.get_center(),
                    buff=0.3, color=YELLOW, stroke_width=3
                )
                gradient_arrows.add(arrow)
        
        # Arrows from hidden to input layer
        for h_neuron in hidden_layer[0]:
            for i_neuron in input_layer[0]:
                arrow = Arrow(
                    h_neuron.get_center(), i_neuron.get_center(),
                    buff=0.3, color=YELLOW, stroke_width=2
                )
                gradient_arrows.add(arrow)
        
        backprop_title = Text("Backpropagation", font_size=20, color=YELLOW).to_edge(UP)
        
        # Animate backpropagation
        self.play(Write(backprop_title), run_time=duration/3)
        self.play(Create(gradient_arrows), run_time=duration)
        self.play(FadeOut(gradient_arrows), FadeOut(backprop_title), run_time=duration/3)
    
    def weight_update_animation(self, input_to_hidden, hidden_to_output, duration=2):
        weight_update_title = Text("Weight Updates", font_size=20, color=GREEN).to_edge(UP)
        self.play(Write(weight_update_title), run_time=duration/3)
        
        # Randomly select some connections to strengthen and some to weaken
        import random
        
        # Update input to hidden weights
        input_hidden_animations = []
        for line in input_to_hidden:
            # Random choice to strengthen or weaken
            if random.random() > 0.5:
                input_hidden_animations.append(
                    line.animate.set_stroke(GREEN_B, width=3)
                )
            else:
                input_hidden_animations.append(
                    line.animate.set_stroke(RED_B, width=0.5)
                )
        
        self.play(*input_hidden_animations, run_time=duration/2)
        
        # Update hidden to output weights
        hidden_output_animations = []
        for line in hidden_to_output:
            # Random choice to strengthen or weaken
            if random.random() > 0.5:
                hidden_output_animations.append(
                    line.animate.set_stroke(GREEN_B, width=3)
                )
            else:
                hidden_output_animations.append(
                    line.animate.set_stroke(RED_B, width=0.5)
                )
        
        self.play(*hidden_output_animations, run_time=duration/2)
        
        # Reset connection colors for next forward pass
        self.play(
            input_to_hidden.animate.set_stroke(GRAY, width=1),
            hidden_to_output.animate.set_stroke(GRAY, width=1),
            FadeOut(weight_update_title),
            run_time=duration/3
        )