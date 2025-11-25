<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Universal Agent Manifests and Cross-Framework State Portability: Recent Updates (2025)

Based on my research of recent developments (May 2024 - August 2025), here's a comprehensive summary of the most significant updates and proposals in universal agent manifests and cross-framework state portability:

### **Major Protocol and Framework Updates**

**Model Context Protocol (MCP) Security and Evolution**

- **Security Concerns**: Multiple security audits in 2025 revealed significant vulnerabilities in MCP implementations, with researchers identifying command injection, path traversal, and SSRF vulnerabilities in 43% of tested MCP servers[^1_1][^1_2][^1_3]
- **MCPSafetyScanner**: First agentic security auditing tool specifically for MCP servers released to address these vulnerabilities[^1_2]
- **Authentication Updates**: June 2025 MCP specification update introduced Resource Indicators (RFC 8707) to prevent token misuse and classified MCP servers as OAuth Resource Servers[^1_4]
- **Active Tool Discovery**: MCP-Zero framework introduced for autonomous tool discovery, achieving 98% reduction in token consumption while maintaining accuracy[^1_5]

**Agent2Agent (A2A) Protocol Maturation**

- **Linux Foundation Adoption**: Google donated the A2A protocol to the Linux Foundation, signaling enterprise-grade standardization[^1_6][^1_7]
- **Enterprise Integration**: Major partners including Salesforce, Box, and Seismic have integrated A2A support, with 50+ technology partners backing the protocol[^1_8][^1_7]
- **Technical Foundation**: A2A now supports multimodal communication (text, audio, video), long-running tasks, and enterprise-grade authentication[^1_9][^1_7]

**AGNTCY Project Launch and Linux Foundation Integration**

- **Linux Foundation Adoption**: July 29, 2025 - AGNTCY project moved to Linux Foundation governance with founding members including Cisco, Dell Technologies, Google Cloud, Oracle, and Red Hat[^1_10][^1_11][^1_12]
- **Open Agent Schema Framework (OASF)**: Standardized schema system for defining AI agent capabilities, interactions, and metadata launched[^1_13][^1_14][^1_15]
- **Agent Connect Protocol (ACP)**: RESTful protocol for agent invocation and configuration, supporting OpenAPI authentication schemes[^1_15][^1_16]
- **65+ Supporting Companies**: Significant industry backing demonstrates commitment to interoperability standards[^1_10]


### **State Serialization and Cross-Framework Portability**

**Letta Agent File (.af) Format**

- **April 2, 2025 Launch**: Letta introduced the Agent File (.af) format as an open standard for serializing stateful AI agents[^1_17][^1_18][^1_19]
- **Comprehensive State Capture**: Includes system prompts, editable memory, tool configurations, and LLM settings in a single portable file[^1_18][^1_20]
- **Cross-Framework Compatibility**: Enables agent transfer between compatible frameworks while preserving memory and behavior[^1_21][^1_19]
- **Example Agents Available**: Deep research agents, customer support agents, and MemGPT agents with pre-configured workflows[^1_18]

**Microsoft Declarative Agent Framework**

- **General Availability**: Microsoft Declarative Agents became GA in late 2024, supporting rapid development through Copilot Studio[^1_22][^1_23]
- **Unified Manifest Approach**: Agents defined through JSON-based specifications with consistent deployment across Microsoft 365 ecosystem[^1_24][^1_23]
- **Enterprise Integration**: Seamless integration with SharePoint, OneDrive, Teams, and other Microsoft services[^1_22]

**Cross-Framework Integration Examples**

- **LangGraph with AutoGen/CrewAI**: Official documentation released showing integration patterns for state preservation and streaming[^1_25]
- **Tool Schema Compatibility**: JSON schemas following OpenAI specification enable tool sharing across LangChain, CrewAI, and Composio frameworks[^1_20]


### **Emerging Standards and RFC-Style Proposals**

**Agent Name Service (ANS)**

- **DNS-Inspired Architecture**: Proposed system for secure agent discovery using PKI certificates and DNS-like naming conventions[^1_26]
- **Protocol-Agnostic**: Supports A2A, MCP, and ACP through modular Protocol Adapter Layer[^1_26]

**Web of Agents Architecture**

- **Interoperability Framework**: Four-component system addressing agent-to-agent messaging, interaction interoperability, state management, and agent discovery[^1_27]
- **Minimal Standards Approach**: Proposes adoption of existing standards rather than creating new protocols[^1_27]

**URI-Based Agent Framework**

- **IETF Draft Proposal**: agent:// protocol for URI-based agent addressing and invocation using RFC 6570 templates[^1_28]
- **Layered Architecture**: Optional components allow minimal or full-featured implementations[^1_28]


### **Validation and Tooling Solutions**

**MCP Security and Validation Tools**

- **MCPSafetyScanner**: First dedicated security tool for auditing MCP server vulnerabilities[^1_2]
- **Enterprise Security Solutions**: Noma Security and other vendors developing MCP-specific security tooling[^1_29]

**Manifest Validation Frameworks**

- **Open Policy Agent Integration**: Conftest and other OPA-based tools being adapted for agent manifest validation[^1_30][^1_31][^1_32]
- **Kubernetes-Inspired Tooling**: Kubeconform and similar tools providing schema validation for agent configurations[^1_33]

**OASF Schema Validation**

- **Development Tools**: Hot-reload capabilities and schema validation built into OASF framework[^1_13][^1_14]
- **Containerized Development Environment**: Taskfile-based workflow for rapid schema development[^1_14]


### **Industry Challenges and Solutions**

**Interoperability Gaps**

- **Fragmented Ecosystems**: Current agents remain "trapped in walled gardens" despite protocol advances[^1_34][^1_35]
- **State Management Complexity**: Different frameworks handle serialization, context windows, and memory management inconsistently[^1_20]
- **Security Standardization**: Lack of unified security practices across frameworks creates vulnerabilities[^1_2][^1_3]

**Proposed Solutions**

- **Hybrid Protocol Adoption**: Combining MCP for tool access, A2A for agent communication, and OASF for discovery[^1_36][^1_15]
- **Just-In-Time Tooling**: Dynamic tool discovery patterns to avoid context window limitations[^1_37]
- **Universal Translation Layers**: I/O Mapper Agents and Semantic Routers for cross-framework compatibility[^1_16]


### **Future Roadmap and Recommendations**

**Near-Term Priorities (2025-2026)**

- **Security Hardening**: Address MCP vulnerabilities and establish security best practices
- **Schema Standardization**: Wider adoption of OASF and similar metadata frameworks
- **Cross-Framework Testing**: Validation tools for agent manifest compatibility

**Long-Term Vision (2026+)**

- **Internet of Agents**: Fully interoperable agent ecosystem with universal discovery and communication
- **Economic Coordination**: Micropayment systems and trust-based collaboration frameworks[^1_38]
- **Enterprise Integration**: Seamless agent deployment across organizational boundaries

This landscape represents a critical inflection point where AI agent interoperability is transitioning from experimental protocols to production-ready standards backed by major technology vendors and open-source foundations.

<div style="text-align: center">⁂</div>

[^1_1]: https://arxiv.org/html/2504.03767v2

[^1_2]: https://arxiv.org/abs/2504.03767

[^1_3]: https://equixly.com/blog/2025/03/29/mcp-server-new-security-nightmare/

[^1_4]: https://auth0.com/blog/mcp-specs-update-all-about-auth/

[^1_5]: https://arxiv.org/html/2506.01056v4

[^1_6]: https://www.ibm.com/think/topics/agent2agent-protocol

[^1_7]: https://www.blott.studio/blog/post/how-the-agent2agent-protocol-a2a-actually-works-a-technical-breakdown

[^1_8]: https://www.youtube.com/watch?v=8DNyqWrBBbI

[^1_9]: https://www.solo.io/topics/ai-infrastructure/what-is-a2a

[^1_10]: https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos

[^1_11]: https://www.forbes.com/sites/moorinsights/2025/07/29/the-agntcy-framework-for-agentic-ai-moves-to-the-linux-foundation/

[^1_12]: https://www.theregister.com/2025/07/30/agntcy_lf_donation/

[^1_13]: https://github.com/agntcy/oasf/blob/main/README.md

[^1_14]: https://github.com/agntcy/oasf

[^1_15]: https://www.linkedin.com/pulse/open-standards-ai-agents-technical-comparison-a2a-mcp-jin-v7qve

[^1_16]: https://docs.agntcy.org

[^1_17]: https://www.evnekquest.com/post/introducing-the-agent-file-af-a-standard-for-stateful-ai-agents

[^1_18]: https://github.com/letta-ai/agent-file

[^1_19]: https://www.letta.com/blog/agent-file

[^1_20]: https://www.letta.com/blog/ai-agents-stack

[^1_21]: https://www.linkedin.com/posts/letta-ai_from-mcp-to-multi-agents-the-top-10-new-activity-7324159999239147520-ev9t

[^1_22]: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-declarative-agent

[^1_23]: https://devblogs.microsoft.com/microsoft365dev/whats-new-for-microsoft-365-copilot-developer-tooling/

[^1_24]: https://arxiv.org/abs/2408.15247

[^1_25]: https://docs.langchain.com/langgraph-platform/autogen-integration

[^1_26]: https://arxiv.org/abs/2505.10609

[^1_27]: https://arxiv.org/abs/2505.21550

[^1_28]: https://www.ietf.org/id/draft-narvaneni-agent-uri-01.html

[^1_29]: https://noma.security/blog/how-model-context-protocol-strengthens-security-for-your-agentic-ai/

[^1_30]: https://faun.pub/validating-argocd-application-manifest-with-open-policy-agent-6590fbe5b859

[^1_31]: https://www.creativesoftware.com/blog-posts/automated-manifest-file-validation-using-open-policy-agent-and-git-hub-actions

[^1_32]: https://tanmay-bhat.github.io/posts/validate-argocd-with-opa/

[^1_33]: https://github.com/HighwayofLife/kubernetes-validation-tools

[^1_34]: https://www.forrester.com/blogs/interoperability-is-key-to-unlocking-agentic-ais-future/

[^1_35]: https://www.linkedin.com/pulse/beyond-walled-agent-gardens-promise-interoperability-muthumari-s-nsnee

[^1_36]: https://arxiv.org/abs/2505.02279

[^1_37]: https://jentic.com/blog/just-in-time-tooling

[^1_38]: https://www.semanticscholar.org/paper/79ae50268af276aa7599f5916131598ac8ff5efe

[^1_39]: https://smujo.id/biodiv/article/view/17644

[^1_40]: https://academic.oup.com/rheumatology/article/doi/10.1093/rheumatology/keaf142.079/8115156

[^1_41]: https://arxiv.org/pdf/2501.00539.pdf

[^1_42]: https://arxiv.org/abs/1905.09808

[^1_43]: https://arxiv.org/pdf/2504.08623.pdf

[^1_44]: https://arxiv.org/pdf/2310.16828.pdf

[^1_45]: http://arxiv.org/pdf/2210.10128.pdf

[^1_46]: http://arxiv.org/pdf/2411.00114.pdf

[^1_47]: https://arxiv.org/html/2404.18074v3

[^1_48]: https://arxiv.org/html/2306.12654

[^1_49]: https://arxiv.org/pdf/2303.10665.pdf

[^1_50]: http://arxiv.org/pdf/2411.05683.pdf

[^1_51]: https://arxiv.org/pdf/2412.11430.pdf

[^1_52]: https://arxiv.org/pdf/2501.06243.pdf

[^1_53]: https://joss.theoj.org/papers/10.21105/joss.00617.pdf

[^1_54]: https://dl.acm.org/doi/pdf/10.1145/3658644.3670346

[^1_55]: https://arxiv.org/pdf/2406.07155v1.pdf

[^1_56]: http://arxiv.org/pdf/2404.08398.pdf

[^1_57]: https://arxiv.org/html/2502.14282v2

[^1_58]: https://a2aprotocol.ai

[^1_59]: https://www.blott.studio/blog/post/mcp-vs-a2a-which-protocol-is-better-for-ai-agents

[^1_60]: https://architecture.learning.sap.com/docs/ref-arch/e5eb3b9b1d/8

[^1_61]: https://rickxie.cn/blog/MCP/

[^1_62]: https://github.com/a2aproject/A2A

[^1_63]: https://addyo.substack.com/p/mcp-what-it-is-and-why-it-matters

[^1_64]: https://radicalbit.ai/resources/blog/a2a-protocol/

[^1_65]: https://hackernoon.com/mcp-servers-101-turn-your-ai-agent-into-a-productive-permissioned-dev-sidekick

[^1_66]: https://arxiv.org/abs/2506.01804

[^1_67]: https://www.youtube.com/watch?v=-5FKg4N8ZbA

[^1_68]: https://xue-guang.com/post/llm-marl/

[^1_69]: https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-1-inter-agent-communication-on-mcp/

[^1_70]: https://bestaiagents.ai/agent/letta

[^1_71]: https://github.com/punkpeye/awesome-mcp-servers

[^1_72]: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/

[^1_73]: https://arxiv.org/abs/2409.08264

[^1_74]: https://www.sciendo.com/article/10.2478/amns-2024-2883

[^1_75]: https://www.techscience.com/JCS/v7n1/62970

[^1_76]: https://ojs.bonviewpress.com/index.php/IJCE/article/view/4500

[^1_77]: https://www.microbiologyresearch.org/content/journal/acmi/10.1099/acmi.0.001020.v3

[^1_78]: https://arxiv.org/abs/2307.12204

[^1_79]: https://www.semanticscholar.org/paper/211c70a4664188e16302e5a8b227eea34488d34f

[^1_80]: http://arxiv.org/pdf/2409.16120.pdf

[^1_81]: http://arxiv.org/pdf/2407.08281.pdf

[^1_82]: https://arxiv.org/pdf/2310.08535.pdf

[^1_83]: http://arxiv.org/pdf/2409.11393.pdf

[^1_84]: https://arxiv.org/html/2408.15247v1

[^1_85]: https://arxiv.org/pdf/2311.17541v2.pdf

[^1_86]: https://arxiv.org/html/2409.08264

[^1_87]: https://arxiv.org/html/2412.08445

[^1_88]: https://arxiv.org/abs/2503.11444

[^1_89]: https://arxiv.org/pdf/2402.15538.pdf

[^1_90]: http://arxiv.org/pdf/2307.07924.pdf

[^1_91]: http://arxiv.org/pdf/2308.00352.pdf

[^1_92]: https://fabrix.ai/blog/some-of-the-open-source-standards-used-with-ai-agents-or-agentic-frameworks/

[^1_93]: https://frontenddogma.com/posts/2025/mastering-cross-framework-state-management-in-micro-frontends/

[^1_94]: https://www.youtube.com/watch?v=1Mp12gefOSU

[^1_95]: https://arxiv.org/pdf/2203.06289.pdf

[^1_96]: https://www.salesforce.com/blog/agent-interoperability/

[^1_97]: https://github.com/tnfe/awesome-state

[^1_98]: https://www.youtube.com/watch?v=YPoDA61_Zag

[^1_99]: https://learnprompting.org/blog/agntcy-open-standard-for-agent-interoperability

[^1_100]: https://maas.io/blog/building-a-cross-framework-ui-with-single-spa-in-maas-2-8

[^1_101]: https://partner.microsoft.com/pl-pl/blog/article/isv-microsoft-ignite-2024

[^1_102]: https://www.ikangai.com/a2a-vs-mcp-ai-standards/

[^1_103]: https://blog.pixelfreestudio.com/state-management-in-micro-frontends-tips-and-strategies/

[^1_104]: https://www.voitanos.io/blog/announce-build-declarative-agents-microsoft-365-copilot-workshop-202503/

[^1_105]: https://hyperframeresearch.com/2025/07/31/is-ai-agent-interoperability-an-achievable-dream/

[^1_106]: https://inspirehep.net/literature/2051376

[^1_107]: https://simondoy.com/2024/12/01/bring-ai-image-generation-to-your-microsoft-365-copilot-declarative-agents/

[^1_108]: https://www.linkedin.com/pulse/brace-internet-agents-learnings-from-latest-standards-wanting-huang-eupqc

[^1_109]: https://arxiv.org/abs/2407.19438

[^1_110]: https://arxiv.org/abs/2411.05828

[^1_111]: https://ieeexplore.ieee.org/document/10350109/

[^1_112]: http://journals.sagepub.com/doi/10.1177/15485129221111171

[^1_113]: http://link.springer.com/10.1007/s10489-015-0690-x

