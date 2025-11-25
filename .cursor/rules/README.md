# Expert Full Stack Developer Rules System

This directory contains a comprehensive rules system that defines three specialized agent roles and their operational guidelines. The system integrates best practices from the `.cursor/knowledge` base and leverages the `nauka.json` learning system for continuous improvement.

## 📋 Rules Structure

The rules are organized in a numbered sequence, with each file focusing on a specific aspect of agent behavior:

### Core Rules (00-10)
- **`00_core_policy.mdc`** - Core policy defining the three agent roles and switching mechanisms
- **`10_knowledge_integration.mdc`** - How the agent integrates and uses the knowledge base

### Specialized Role Rules (20-50)
- **`20_qa_manager.mdc`** - QA Manager role rules with nauka.json integration
- **`30_plan_mode_writer.mdc`** - LeadTechnicalWriter rules for Plan Mode operations
- **`40_full_stack_best_practices.mdc`** - Full-stack development best practices compilation
- **`50_learning_system.mdc`** - Learning system integration with nauka.json

### Future Extensions (60-95)
- **`60_context_management.mdc`** - Advanced context management patterns
- **`70_error_recovery.mdc`** - Error recovery and debugging patterns
- **`80_cost_optimization.mdc`** - Cost and performance optimization strategies
- **`90_code_review_patterns.mdc`** - Code review guidelines and quality assurance
- **`95_refactoring_strategies.mdc`** - Safe refactoring patterns and strategies

## 🎭 Agent Roles

### Expert Full Stack Developer (Default)
**Primary Focus**: Code implementation, architecture decisions, refactoring
- **Activation**: Default role for all development tasks
- **Responsibilities**: Writing code, debugging, performance optimization
- **Key Rules**: `00_core_policy.mdc`, `40_full_stack_best_practices.mdc`

### QA Manager
**Primary Focus**: Quality assurance, testing strategy, bug prevention
- **Activation**: Automatic when running tests, debugging failures, code review
- **Responsibilities**: Test automation, quality gates, root cause analysis
- **Key Rules**: `20_qa_manager.mdc`, `50_learning_system.mdc`

### LeadTechnicalWriter/Principal Technical Writer
**Primary Focus**: Technical documentation, planning, structured communication
- **Activation**: Automatic in Plan Mode (Shift+Tab), documentation tasks
- **Responsibilities**: Plan creation, technical writing, stakeholder communication
- **Key Rules**: `30_plan_mode_writer.mdc`, `10_knowledge_integration.mdc`

## 🔄 Role Switching Mechanisms

### Automatic Activation Triggers

| Role | Trigger Conditions | Key Indicators |
|------|-------------------|----------------|
| **QA Manager** | `pytest`, `npm test`, test failures, debugging sessions | Test execution, error analysis, quality checks |
| **LeadTechnicalWriter** | Shift+Tab (Plan Mode), documentation requests | Plan creation, technical writing, stakeholder communication |
| **Expert Developer** | Code implementation, refactoring, feature development | Code writing, architecture decisions, optimization |

### Manual Role Switching
Users can explicitly request role activation:
```
"Switch to QA Manager mode for this testing task"
"Activate LeadTechnicalWriter for documentation"
"Use Expert Developer for implementation"
```

### Role Collaboration Workflow
Complex tasks often require role collaboration:
1. **Planning Phase**: LeadTechnicalWriter creates structured plan
2. **Implementation Phase**: Expert Developer executes the plan
3. **Quality Phase**: QA Manager validates and tests the implementation
4. **Documentation Phase**: LeadTechnicalWriter documents the solution

## 📚 Knowledge Base Integration

### Knowledge Sources Hierarchy
1. **Tier 1**: `unified_cursor_agent_pack.json` - Core Cursor practices
2. **Tier 2**: `unified_llm_reasoning.json` - Reasoning strategies (ToT, CoT, GoT)
3. **Tier 3**: `cursor_2_0_best_practices.json` - Plan Mode practices
4. **Tier 4**: Domain-specific knowledge (Backend.md, testing, Docker)

### Query Strategies
- **codebase_search**: Project-specific context and implementation details
- **read_file**: Direct knowledge access for best practices and patterns
- **grep**: Finding specific code patterns and dependencies

## 🧠 Learning System (nauka.json)

### Automatic Integration
The agent automatically consults `nauka.json` before:
- Starting new implementations
- Running tests
- Debugging issues
- Making architectural decisions

### Lesson Categories
- **Import Errors**: ModuleNotFoundError, ImportError patterns
- **Async Issues**: Coroutine errors, context issues
- **Singleton Problems**: Duplicate initialization, resource conflicts
- **Model Errors**: Pydantic attribute issues, type confusion
- **Architecture Changes**: Refactoring impacts, breaking changes

### Learning Workflow
1. **Pre-Action**: Check relevant lessons and apply prevention strategies
2. **During Action**: Monitor for known issue patterns
3. **Post-Action**: Update lessons with new experiences and solutions

## 📖 How to Use These Rules

### For Users
1. **Normal Development**: Agent operates in Expert Developer mode by default
2. **Testing Tasks**: QA Manager automatically activates for quality assurance
3. **Complex Planning**: Use Shift+Tab to activate LeadTechnicalWriter in Plan Mode
4. **Specific Needs**: Explicitly request role switching when needed

### For Development
1. **Code Implementation**: Follow full-stack best practices from `40_full_stack_best_practices.mdc`
2. **Quality Assurance**: Apply QA Manager rules from `20_qa_manager.mdc`
3. **Planning**: Use LeadTechnicalWriter guidelines from `30_plan_mode_writer.mdc`
4. **Learning**: Leverage nauka.json integration for continuous improvement

### For Maintenance
1. **Rule Updates**: Modify individual `.mdc` files as practices evolve
2. **Knowledge Updates**: Update knowledge base references when new practices emerge
3. **Learning Enhancement**: Add new lessons to nauka.json after resolving issues
4. **Consistency Checks**: Run verification to ensure rule coherence

## 🔧 Rule File Format

All rule files use Markdown format (`.mdc`) with structured sections:

```markdown
# Rule Category Title

## Section Header
Content and guidelines...

### Subsection
Detailed implementation guidance...

#### Code Examples
```language
// Code examples with syntax highlighting
```

**Key Points:**
- Important information highlighted
- Structured lists and tables
- Cross-references to other rules
```

## 📊 Quality Assurance

### Rule Consistency Checks
- [ ] All roles clearly defined with non-overlapping responsibilities
- [ ] Role switching triggers are unambiguous and comprehensive
- [ ] Knowledge integration references are current and accurate
- [ ] Learning system integration is automatic and effective
- [ ] Best practices are drawn from authoritative sources

### Performance Metrics
- **Role Switching Accuracy**: Correct role activation based on context
- **Knowledge Application**: Successful use of best practices from knowledge base
- **Learning Effectiveness**: Reduction in repeated issues through nauka.json
- **Plan Quality**: Improvement in plan comprehensiveness and success rates

## 🔄 Version Control and Updates

### Rule Evolution
- **Version History**: Track changes to individual rules
- **Backward Compatibility**: Ensure updates don't break existing functionality
- **Deprecation Notices**: Clearly mark outdated practices
- **Migration Guides**: Provide guidance for significant rule changes

### Knowledge Base Synchronization
- **Automatic Updates**: Rules reference current knowledge base versions
- **Manual Reviews**: Periodic review of knowledge references
- **Impact Assessment**: Evaluate how knowledge changes affect rules
- **Update Notifications**: Alert when knowledge base changes require rule updates

## 🚨 Emergency Procedures

### Rule Conflicts
If conflicting rules are discovered:
1. **Identify Conflict**: Document the specific contradiction
2. **Priority Resolution**: Apply core policy rules (`00_core_policy.mdc`) as final authority
3. **Rule Update**: Modify conflicting rules to resolve the issue
4. **Documentation**: Update this README with resolution rationale

### Missing Coverage
For scenarios not covered by current rules:
1. **Gap Analysis**: Document the uncovered scenario
2. **Temporary Guidance**: Provide immediate guidance based on best practices
3. **Rule Extension**: Add new rules or extend existing ones
4. **Knowledge Update**: Consider updating knowledge base if needed

## 📈 Future Enhancements

### Planned Extensions
- **Context Management**: Advanced context scoping and optimization
- **Error Recovery**: Systematic debugging and recovery patterns
- **Cost Optimization**: Token usage and performance optimization
- **Code Review**: Structured code review processes and checklists
- **Refactoring**: Safe refactoring strategies and patterns

### Continuous Improvement
- **User Feedback**: Incorporate user experience improvements
- **Performance Monitoring**: Track rule effectiveness and usage patterns
- **Industry Updates**: Integrate emerging best practices and technologies
- **Automation**: Develop automated rule validation and updating

## 🤝 Contributing to Rules

### Rule Development Process
1. **Identify Need**: Recognize gap in current rule coverage
2. **Research**: Consult knowledge base and industry best practices
3. **Draft Rules**: Create comprehensive rule documentation
4. **Peer Review**: Validate rules against existing system
5. **Integration**: Add rules to appropriate numbered file
6. **Documentation**: Update this README with new rule information

### Quality Standards
- **Completeness**: Rules should cover all aspects of the targeted scenario
- **Clarity**: Rules must be understandable and actionable
- **Consistency**: Rules should align with existing system architecture
- **Maintainability**: Rules should be easy to update and extend
- **Effectiveness**: Rules should demonstrably improve agent performance

## 📞 Support and Troubleshooting

### Common Issues
- **Role Not Switching**: Check trigger conditions in `00_core_policy.mdc`
- **Knowledge Not Found**: Verify knowledge base references in `10_knowledge_integration.mdc`
- **Learning Not Working**: Check nauka.json format and integration in `50_learning_system.mdc`
- **Plan Quality Issues**: Review Plan Mode guidelines in `30_plan_mode_writer.mdc`

### Getting Help
1. **Rule Reference**: Check specific rule files for detailed guidance
2. **Knowledge Base**: Consult `.cursor/knowledge` for underlying principles
3. **Learning System**: Review `nauka.json` for historical solutions
4. **Community Resources**: Reference Cursor documentation and community forums

---

## 📈 System Health Dashboard

### Current Status
- ✅ **Rules Created**: 11/11 complete rules system implemented
- ✅ **Roles Defined**: 3 roles with clear responsibilities
- ✅ **Knowledge Integration**: Full knowledge base integration
- ✅ **Learning System**: nauka.json automatic integration
- 🔄 **Testing**: Rules validation in progress

### Next Milestones
- Complete remaining 5 rule files (60-95)
- Implement automated rule validation
- Establish rule update procedures
- Create user training materials

---

*This rules system represents a comprehensive framework for expert-level AI agent operation. Regular updates and community contributions are essential for maintaining effectiveness and relevance.*
