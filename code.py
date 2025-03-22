
from manim import *
import numpy as np
from scipy.stats import norm, binom, poisson, expon

class ProbabilityDistributions(Scene):
    def construct(self):
        title = Text("Key Probability Distributions").scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))
        
        # Discrete Distributions Section
        discrete_title = Text("Discrete Distributions", color=BLUE).scale(0.7)
        discrete_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(discrete_title))
        
        # Bernoulli
        bernoulli = VGroup(
            Text("Bernoulli(p)", color=GREEN).scale(0.6),
            MathTex(r"P(X=x) = p^x(1-p)^{1-x}, x \in \{0,1\}").scale(0.5),
            MathTex(r"\mu = p, \sigma^2 = p(1-p)").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bernoulli.next_to(discrete_title, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(bernoulli))
        
        # Binomial
        binomial = VGroup(
            Text("Binomial(n, p)", color=GREEN).scale(0.6),
            MathTex(r"P(X=k) = {n \choose k}p^k(1-p)^{n-k}").scale(0.5),
            MathTex(r"\mu = np, \sigma^2 = np(1-p)").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        binomial.next_to(bernoulli, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(binomial))
        
        # Poisson
        poisson_dist = VGroup(
            Text("Poisson(λ)", color=GREEN).scale(0.6),
            MathTex(r"P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}").scale(0.5),
            MathTex(r"\mu = \lambda, \sigma^2 = \lambda").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        poisson_dist.next_to(binomial, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(poisson_dist))
        
        self.wait()
        self.play(FadeOut(bernoulli, binomial, poisson_dist, discrete_title))
        
        # Continuous Distributions Section
        continuous_title = Text("Continuous Distributions", color=RED).scale(0.7)
        continuous_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(continuous_title))
        
        # Visualize Normal Distribution
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            axis_config={"include_tip": False},
            x_length=6,
            y_length=3
        )
        axes.next_to(continuous_title, DOWN, buff=0.5)
        
        normal_label = Text("Normal Distribution", color=RED).scale(0.5)
        normal_label.next_to(axes, UP)
        
        normal_func = lambda x: norm.pdf(x, 0, 1)
        normal_graph = axes.plot(normal_func, color=BLUE)
        normal_eq = MathTex(r"f(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}").scale(0.5)
        normal_eq.next_to(axes, DOWN)
        
        self.play(Create(axes), Write(normal_label))
        self.play(Create(normal_graph), Write(normal_eq))
        
        self.wait()
        
        # Show Central Limit Theorem
        clt_title = Text("Central Limit Theorem").scale(0.7)
        clt_formula = MathTex(r"\frac{\sum_{i=1}^{n}X_i - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} N(0,1)").scale(0.6)
        
        clt_group = VGroup(clt_title, clt_formula).arrange(DOWN, buff=0.3)
        
        self.play(FadeOut(axes, normal_graph, normal_label, normal_eq, continuous_title))
        self.play(Write(clt_group))
        
        self.wait(2)
        self.play(FadeOut(clt_group, title))
