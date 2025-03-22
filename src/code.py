
from manim import *
import numpy as np
from scipy.stats import norm, binom, poisson, expon

class ProbabilityDistributions(Scene):
    def construct(self):
        self.show_title()
        self.show_discrete_distributions()
        self.show_continuous_distributions()
        self.show_relationships()
    
    def show_title(self):
        title = Text("Probability Distributions").scale(1.2)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        self.wait(0.5)
    
    def show_discrete_distributions(self):
        discrete_title = Text("Discrete Distributions").scale(0.8).next_to(ORIGIN, UP).to_edge(LEFT)
        self.play(Write(discrete_title))
        
        # Bernoulli
        bern_p = 0.6
        bern_vals = [0, 1]
        bern_probs = [1-bern_p, bern_p]
        bern_chart = self.create_bar_chart(bern_vals, bern_probs, title="Bernoulli(p=0.6)")
        bern_chart.scale(0.7).next_to(discrete_title, DOWN, buff=0.5).to_edge(LEFT)
        
        # Binomial
        bin_n, bin_p = 10, 0.4
        bin_vals = list(range(11))
        bin_probs = [binom.pmf(k, bin_n, bin_p) for k in bin_vals]
        bin_chart = self.create_bar_chart(bin_vals, bin_probs, title="Binomial(n=10, p=0.4)")
        bin_chart.scale(0.7).next_to(bern_chart, RIGHT, buff=1)
        
        # Poisson
        pois_lambda = 3
        pois_vals = list(range(10))
        pois_probs = [poisson.pmf(k, pois_lambda) for k in pois_vals]
        pois_chart = self.create_bar_chart(pois_vals, pois_probs, title="Poisson(λ=3)")
        pois_chart.scale(0.7).next_to(bern_chart, DOWN, buff=1)
        
        self.play(Create(bern_chart), Create(bin_chart), Create(pois_chart))
        self.wait()
        
        self.play(FadeOut(discrete_title, bern_chart, bin_chart, pois_chart))
    
    def show_continuous_distributions(self):
        cont_title = Text("Continuous Distributions").scale(0.8).next_to(ORIGIN, UP).to_edge(LEFT)
        self.play(Write(cont_title))
        
        # Normal
        normal_graph = self.create_pdf_graph(lambda x: norm.pdf(x, 0, 1), 
                                             x_range=[-4, 4, 0.1], 
                                             color=BLUE, 
                                             title="Normal(μ=0, σ²=1)")
        normal_graph.scale(0.7).next_to(cont_title, DOWN, buff=0.5).to_edge(LEFT)
        
        # Exponential
        exp_lambda = 1
        exp_graph = self.create_pdf_graph(lambda x: expon.pdf(x, scale=1/exp_lambda), 
                                          x_range=[0, 5, 0.1], 
                                          color=GREEN, 
                                          title=f"Exponential(λ={exp_lambda})")
        exp_graph.scale(0.7).next_to(normal_graph, RIGHT, buff=1)
        
        self.play(Create(normal_graph), Create(exp_graph))
        self.wait()
        
        self.play(FadeOut(cont_title, normal_graph, exp_graph))
    
    def show_relationships(self):
        title = Text("Important Relationships").scale(0.8)
        self.play(Write(title))
        
        relationships = VGroup(
            Text("• Sum of n Bernoulli(p) → Binomial(n,p)", font_size=24),
            Text("• Binomial with n→∞, p→0, np=λ → Poisson(λ)", font_size=24),
            Text("• Sum of independent Normal → Normal", font_size=24),
            Text("• Central Limit Theorem", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        relationships.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(relationships))
        self.wait(2)
        
        self.play(FadeOut(title, relationships))
    
    def create_bar_chart(self, x_values, probabilities, title=""):
        bars = VGroup()
        max_height = 3
        bar_width = 0.4
        
        # Normalize to make tallest bar of height max_height
        scale = max_height / max(probabilities) if max(probabilities) > 0 else 1
        
        for i, (x, p) in enumerate(zip(x_values, probabilities)):
            bar = Rectangle(
                height=p * scale,
                width=bar_width,
                fill_opacity=0.8,
                fill_color=BLUE,
                stroke_color=WHITE
            ).move_to(np.array([i * (bar_width + 0.1), p * scale / 2, 0]))
            
            bars.add(bar)
        
        bars.move_to(ORIGIN)
        
        chart_title = Text(title, font_size=24).next_to(bars, UP)
        
        return VGroup(bars, chart_title)
    
    def create_pdf_graph(self, func, x_range=[-10, 10, 0.1], color=BLUE, title=""):
        axes = Axes(
            x_range=[x_range[0], x_range[1]],
            y_range=[0, func((x_range[0] + x_range[1]) / 2) * 1.5],
            axis_config={"include_tip": False},
        )
        
        graph = axes.plot(func, color=color)
        
        graph_title = Text(title, font_size=24).next_to(axes, UP)
        
        return VGroup(axes, graph, graph_title)
